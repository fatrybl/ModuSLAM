from collections.abc import Iterable, Sequence

import numpy as np
import open3d as o3d

from src.custom_types.aliases import Matrix4x4
from src.custom_types.numpy import Matrix4x4 as NumpyMatrix4x4
from src.custom_types.numpy import MatrixNx3
from src.external.metrics.base import Metrics
from src.external.metrics.modified_mom.config import LidarConfig
from src.external.metrics.modified_mom.metrics import mom
from src.measurement_storage.measurements.pose_odometry import OdometryWithElements
from src.moduslam.data_manager.batch_factory.data_objects import Element
from src.moduslam.data_manager.batch_factory.factory import BatchFactory
from src.moduslam.frontend_manager.main_graph.data_classes import GraphElement
from src.moduslam.frontend_manager.main_graph.edges.base import Edge
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.moduslam.map_manager.map_factories.lidar_map.config import (
    LidarPointCloudConfig,
)
from src.moduslam.map_manager.map_factories.lidar_map.utils import (
    create_pose_edges_table,
    map_elements2vertices,
    values_to_array,
)
from src.moduslam.map_manager.map_factories.utils import (
    fill_elements,
    filter_array,
    transform_pointcloud,
)
from src.moduslam.sensors_factory.sensors import Lidar3D
from src.utils.auxiliary_objects import identity4x4
from src.utils.exceptions import ExternalModuleException
from src.utils.ordered_set import OrderedSet


class PlaneOrthogonality(Metrics):
    """Computes the MOM metrics:
    https://www.researchgate.net/publication/352572583_Be_your_own_Benchmark_No-Reference_Trajectory_Metric_on_Registered_Point_Clouds.
    """

    def __init__(self, point_cloud_config: LidarPointCloudConfig, batch_factory: BatchFactory):
        """
        Args:
            point_cloud_config: a configuration for processing point clouds.

            batch_factory: a factory for creating elements.
        """
        self._point_cloud_config = point_cloud_config
        self._mom_config = LidarConfig()

        self._batch_factory = batch_factory

    def compute(self, connections: dict[Vertex, set[Edge]], elements: list[GraphElement]) -> float:
        """Computes the MOM metrics.

        Args:
            connections: connections between vertices.

            elements: new graph elements.

        Returns:
            MOM metric value.
        """
        new_edges = [el.edge for el in elements]
        poses = self._get_poses(new_edges)

        pose_arrays = [np.array(p.value) for p in poses]

        poses_with_edges = {p: connections[p] for p in poses}

        point_clouds = self._create_point_clouds(poses_with_edges)

        value = self._compute_mom(pose_arrays, point_clouds, self._mom_config)

        return value

    @staticmethod
    def _get_poses(edges: Sequence[Edge]) -> OrderedSet[Pose]:
        """Gets poses used to create the edges with Lidar odometry.

        Args:
            edges: graph edges.

        Returns:
            poses.
        """
        poses = OrderedSet[Pose]()

        for edge in edges:
            m = edge.measurement

            if isinstance(edge, PoseOdometry) and isinstance(m, OdometryWithElements):
                poses.add(edge.vertex1)
                poses.add(edge.vertex2)

        return poses

    def _create_point_clouds(
        self, connections: dict[Pose, set[Edge]]
    ) -> list[o3d.geometry.PointCloud]:
        """Creates clouds of raw lidar points for the given poses.

        Args:
            connections: table of poses and connected edges.

        Returns:
            point clouds.
        """
        table1 = create_pose_edges_table(connections)

        table2 = map_elements2vertices(table1)

        table3 = fill_elements(table2, self._batch_factory)

        point_clouds: list[o3d.geometry.PointCloud] = []

        for pose, elements in table3.items():
            cloud = self._create_point_cloud(elements, self._point_cloud_config)
            point_clouds.append(cloud)

        return point_clouds

    @staticmethod
    def _create_point_cloud(
        elements: Iterable[Element], config: LidarPointCloudConfig
    ) -> o3d.geometry.PointCloud:
        """Creates a 3D point cloud array.

        Args:
            elements: elements with lidar measurements.

            config: a configuration for point cloud creation.

        Returns:
            a 3D point cloud array [Nx3].
        """
        point_clouds = []

        for element in elements:
            sensor = element.measurement.sensor
            values = element.measurement.values

            if isinstance(sensor, Lidar3D) and values is not None:
                tf = sensor.tf_base_sensor
                cloud = PlaneOrthogonality._create_3d_points(tf, values, config)
                point_clouds.append(cloud)

        pcd_array = np.vstack(point_clouds)
        o3d_cloud = o3d.geometry.PointCloud()
        o3d_cloud.points = o3d.utility.Vector3dVector(pcd_array)
        return o3d_cloud

    @staticmethod
    def _create_3d_points(
        tf: Matrix4x4, values: tuple[float, ...], config: LidarPointCloudConfig
    ) -> MatrixNx3:
        """Creates a [N,3] matrix with 3D coordinates of points.

        Args:
            tf: a transformation matrix.

            values: raw lidar point cloud data.

            config: a configuration for lidar point cloud.

        Returns:
            a [N,3] matrix .
        """
        i4x4 = np.array(identity4x4)
        tf_array = np.array(tf)
        points = values_to_array(values, config.num_channels)
        points = filter_array(points, config.min_range, config.max_range)
        points[:, 3] = 1  # ignore intensity channel and make SE(3) compatible.
        points = transform_pointcloud(i4x4, tf_array, points)
        points = points[:, :-1]  # remove unnecessary 4-th dimension.
        return points

    @staticmethod
    def _compute_mom(
        poses: list[NumpyMatrix4x4], point_clouds: list[MatrixNx3], config: LidarConfig
    ) -> float:
        """Computes the MOM metrics.

        Args:
            poses: SE(3) poses.

            point_clouds: a list of arrays with [Nx3] point clouds.

            config: a configuration for MOM metric.

        Returns:
            MOM metric value.

        Raises:
            ExternalModuleException: if the external MOM module fails to compute the metric.
        """
        try:
            value = mom(point_clouds, poses, config=config)
        except Exception as e:
            raise ExternalModuleException(e)

        return value
