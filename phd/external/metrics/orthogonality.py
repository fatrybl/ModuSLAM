from collections.abc import Iterable

import numpy as np
import open3d as o3d
from map_metrics.config import LidarConfig
from map_metrics.metrics import mom

from phd.external.metrics.base import Metrics
from phd.moduslam.custom_types.aliases import Matrix4x4
from phd.moduslam.custom_types.numpy import Matrix4x4 as NumpyMatrix4x4
from phd.moduslam.custom_types.numpy import MatrixNx3
from phd.moduslam.data_manager.batch_factory.config_factory import (
    get_config as get_bf_config,
)
from phd.moduslam.data_manager.batch_factory.data_objects import Element
from phd.moduslam.data_manager.batch_factory.factory import BatchFactory
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.map_manager.map_factories.lidar_map.config import (
    LidarPointCloudConfig,
)
from phd.moduslam.map_manager.map_factories.lidar_map.config_factory import (
    get_config as get_pointcloud_config,
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


class PlaneOrthogonality(Metrics):

    def __init__(self):
        bf_config = get_bf_config()
        self._point_cloud_config = get_pointcloud_config()
        self._mom_config = LidarConfig()
        self._batch_factory = BatchFactory(bf_config)

    def compute(self, storage: VertexStorage, connections: dict[Vertex, set[Edge]]) -> float:
        """Computes the MOM metrics.

        Args:
            storage: a storage with vertices.

            connections: connections between vertices.

        Returns:
            MOM metric value.
        """

        poses = storage.get_vertices(Pose)
        pose_arrays = [np.array(pose.value) for pose in poses]

        point_clouds = self._create_point_clouds(poses, connections)

        value = self._compute_mom(pose_arrays, point_clouds, self._mom_config)
        return value

    def _create_point_clouds(
        self, poses: Iterable[Pose], connections: dict[Vertex, set[Edge]]
    ) -> list[o3d.geometry.PointCloud]:
        """Creates clouds of raw lidar points for the given poses.

        Args:
            poses: poses to create point clouds for.

            connections: connections between vertices.

        Returns:
            point clouds.
        """
        table1 = {p: connections[p] for p in poses}

        table2 = create_pose_edges_table(table1)

        table3 = map_elements2vertices(table2)

        table4 = fill_elements(table3, self._batch_factory)

        point_clouds: list[o3d.geometry.PointCloud] = []

        for pose, elements in table4.items():
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
        except Exception:
            raise ExternalModuleException

        return value
