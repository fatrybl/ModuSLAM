import logging
from collections.abc import Iterable, Sequence

import numpy as np
import open3d as o3d

from phd.external.metrics.base import Metrics
from phd.logger.logging_config import frontend_manager
from phd.measurement_storage.measurements.pose_odometry import OdometryWithElements
from phd.modified_mom.config import LidarConfig
from phd.modified_mom.metrics import mom
from phd.moduslam.custom_types.aliases import Matrix4x4
from phd.moduslam.custom_types.numpy import Matrix4x4 as NumpyMatrix4x4
from phd.moduslam.custom_types.numpy import MatrixNx3
from phd.moduslam.data_manager.batch_factory.data_objects import Element
from phd.moduslam.data_manager.batch_factory.factory import BatchFactory
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.new_element import GraphElement
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.map_manager.map_factories.lidar_map.config import (
    LidarPointCloudConfig,
)
from phd.moduslam.map_manager.map_factories.lidar_map.utils import (
    create_pose_edges_table,
    map_elements2vertices,
    values_to_array,
)
from phd.moduslam.map_manager.map_factories.utils import (
    fill_elements,
    filter_array,
    transform_pointcloud,
)
from phd.moduslam.sensors_factory.sensors import Lidar3D
from phd.utils.auxiliary_objects import identity4x4
from phd.utils.exceptions import ExternalModuleException
from phd.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


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
        self._mom_config.EIGEN_SCALE = 10
        self._mom_config.MIN_CLUST_SIZE = 5
        self._mom_config.KNN_RAD = 1.5

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
        point_cloud = np.empty(shape=(0, 3))

        for element in elements:
            sensor = element.measurement.sensor
            values = element.measurement.values

            if isinstance(sensor, Lidar3D) and values is not None:
                tf = sensor.tf_base_sensor
                points = PlaneOrthogonality._create_3d_points(tf, values, config)
                point_cloud = np.vstack((point_cloud, points))

        o3d_cloud = o3d.geometry.PointCloud()
        o3d_cloud.points = o3d.utility.Vector3dVector(point_cloud)
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
        points[:, 3] = 1  # ignore intensity channel and make SE(3) compatible.
        points = filter_array(points, config.min_range, config.max_range)
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
