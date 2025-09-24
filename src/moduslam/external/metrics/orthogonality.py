from collections.abc import Iterable, Sequence
from typing import TypeAlias

import numpy as np
import open3d as o3d

from moduslam.custom_types.numpy import Matrix4x4 as NumpyMatrix4x4
from moduslam.custom_types.numpy import MatrixNx3
from moduslam.data_manager.batch_factory.data_objects import Element
from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.external.metrics.base import Metrics
from moduslam.external.metrics.modified_mom.config import HdbscanConfig, LidarConfig
from moduslam.external.metrics.modified_mom.hdbscan_planes import (
    extract_orthogonal_subsets,
)
from moduslam.external.metrics.modified_mom.metrics import mom
from moduslam.external.metrics.utils import median
from moduslam.frontend_manager.main_graph.data_classes import GraphElement
from moduslam.frontend_manager.main_graph.edges.base import Edge
from moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from moduslam.frontend_manager.main_graph.vertices.base import Vertex
from moduslam.frontend_manager.main_graph.vertices.custom import Pose
from moduslam.map_manager.factories.lidar_map.config import (
    LidarPointCloudConfig,
)
from moduslam.map_manager.factories.lidar_map.utils import (
    create_point_cloud_from_element,
    create_pose_edges_table,
    map_elements2vertices,
)
from moduslam.map_manager.factories.utils import fill_elements
from moduslam.measurement_storage.measurements.pose_odometry import OdometryWithElements
from moduslam.sensors_factory.sensors import Lidar3D
from moduslam.utils.exceptions import ExternalModuleException
from moduslam.utils.ordered_set import OrderedSet

Cloud: TypeAlias = o3d.geometry.PointCloud


class PlaneOrthogonality(Metrics):
    """Computes the MOM metrics:
    https://www.researchgate.net/publication/352572583_Be_your_own_Benchmark_No-Reference_Trajectory_Metric_on_Registered_Point_Clouds.
    """

    def __init__(self, point_cloud_config: LidarPointCloudConfig, batch_factory: BatchFactory):
        """
        Args:
            point_cloud_config: a configuration for processing point clouds.

            batch_factory: a factory to create elements with raw lidar measurements.
        """
        self._point_cloud_config = point_cloud_config
        self._mom_config = LidarConfig()
        self._plane_detection_config = HdbscanConfig()
        self._batch_factory = batch_factory

    def compute(
        self, connections: dict[Vertex, set[Edge]], graph_elements: list[GraphElement]
    ) -> float:
        """Computes the MOM metrics.

        Args:
            connections: connections between vertices.

            graph_elements: graph elements with poses.

        Returns:
            MOM metric value.
        """
        new_edges = [el.edge for el in graph_elements]
        poses = self._get_poses(new_edges)

        pose_arrays = [np.array(p.value) for p in poses]

        poses_with_edges = {p: connections[p] for p in poses}

        poses_with_elements = self._create_pose_elements_table(
            self._batch_factory, poses_with_edges
        )

        clouds = self._create_clouds_to_evaluate(poses_with_elements)
        cloud = self._create_central_cloud(poses_with_elements)

        value = self._compute_mom(
            pose_arrays, clouds, cloud, self._mom_config, self._plane_detection_config
        )

        return value

    def _create_central_cloud(self, table: dict[Pose, list[Element]]) -> Cloud:
        """Creates a point cloud of 1 lidar measurement for the pose with central index.

        Args:
            table: a table with poses and the corresponding raw lidar measurements.

        Returns:
            a 3D point cloud.
        """
        items = list(table.items())
        pose_0, _ = items[0]
        pose_i, elements = median(items)
        element = elements[0]

        current_pose = np.array(pose_i.value)
        first_pose = np.array(pose_0.value)

        tf = np.linalg.inv(first_pose) @ current_pose

        cloud = create_point_cloud_from_element(element, self._point_cloud_config)
        cloud.transform(tf)

        return cloud

    def _create_clouds_to_evaluate(self, table: dict[Pose, list[Element]]) -> list[Cloud]:
        """Creates a list of 3D point clouds to evaluate.

        Args:
            table: a table with poses and the corresponding raw lidar measurements.

        Returns:
            a list of 3D point clouds.
        """
        point_clouds: list[Cloud] = []

        for pose, elements in table.items():
            cloud = self._aggregate_point_cloud(elements, self._point_cloud_config)
            point_clouds.append(cloud)

        return point_clouds

    @classmethod
    def _aggregate_point_cloud(
        cls, elements: Iterable[Element], config: LidarPointCloudConfig
    ) -> Cloud:
        """Creates a 3D point cloud from multiple elements.

        Args:
            elements: elements with lidar measurements.

            config: a configuration for point cloud creation.

        Returns:
            a 3D point cloud.
        """
        o3d_cloud = Cloud()

        for element in elements:
            cloud = create_point_cloud_from_element(element, config)
            o3d_cloud += cloud

        return o3d_cloud

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
                sensor = m.elements[0].measurement.sensor

                if isinstance(sensor, Lidar3D):
                    poses.add(edge.vertex1)
                    poses.add(edge.vertex2)

        return poses

    @staticmethod
    def _create_pose_elements_table(
        factory: BatchFactory, connections: dict[Pose, set[Edge]]
    ) -> dict[Pose, list[Element]]:
        """Creates a table with poses and the corresponding raw elements with Lidar
        measurements.

        Args:
            factory: a factory for creating elements with raw lidar measurements.

            connections: table of poses and connected edges.

        Returns:
            a table with poses and elements.
        """
        table1 = create_pose_edges_table(connections)

        table2 = map_elements2vertices(table1)

        table3 = fill_elements(table2, factory)

        return table3

    @staticmethod
    def _compute_mom(
        poses: list[NumpyMatrix4x4],
        point_clouds: list[MatrixNx3],
        evaluation_cloud: MatrixNx3,
        mom_config: LidarConfig,
        plane_detection_config: HdbscanConfig,
    ) -> float:
        """Computes the MOM metrics:
        1. Extracts orthogonal subsets from evaluation point cloud.
        2. Computes mom value for the given point clouds and poses.


        Args:
            poses: SE(3) poses.

            point_clouds: a list of arrays with [Nx3] point clouds.

            evaluation_cloud: a [Nx3] point cloud to extract orthogonal planes from.

            mom_config: a configuration for MOM metric.

        Returns:
            MOM metric value.

        Raises:
            ExternalModuleException: if the external MOM module fails to compute the metric.
        """
        try:
            # o3d.visualization.draw_geometries(point_clouds)
            # o3d.visualization.draw_geometries([evaluation_cloud])
            orth_subsets = extract_orthogonal_subsets(
                evaluation_cloud, mom_config, plane_detection_config
            )

            # cloud = o3d.geometry.PointCloud()
            # for pcd in point_clouds:
            #     cloud += pcd
            # visualize_point_cloud_with_subsets(evaluation_cloud, orth_subsets)

            value = mom(point_clouds, poses, mom_config, plane_detection_config, orth_subsets)
            return value

        except Exception as e:
            raise ExternalModuleException(e)
