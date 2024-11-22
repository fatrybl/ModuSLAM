from phd.bridge.edge_factories.factory_protocol import EdgeFactory, VertexWithStatus
from phd.bridge.edge_factories.noise_models import pose_block_diagonal_noise_model
from phd.bridge.edge_factories.utils import get_cluster, get_new_items
from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.moduslam.frontend_manager.main_graph.vertices.custom import identity4x4
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: PoseMeasurement
    ) -> GraphElement:
        """Creates a new edge with prior SE(3) pose factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a measurement with pose SE(3).

        Returns:
            a new element.
        """
        t = measurement.timestamp
        vertex = cls._get_pose_with_status(graph.vertex_storage, clusters, t)

        edge = cls._create_edge(vertex.instance, measurement)

        new_vertices = get_new_items([vertex])

        element = GraphElement(edge, new_vertices)
        return element

    @classmethod
    def _get_pose_with_status(
        cls, storage: VertexStorage, clusters: dict[VertexCluster, TimeRange], timestamp
    ) -> VertexWithStatus[PoseVertex]:
        """Gets a pose with the status.

        Args:
            storage: a global storage with poses.

            clusters: clusters with time ranges.

            timestamp: a timestamp.

        Returns:
            a pose with the status.
        """
        existing_cluster = storage.get_cluster(timestamp)
        last_pose = storage.get_latest_vertex(PoseVertex)

        if existing_cluster:
            cluster = existing_cluster

        else:
            cluster = get_cluster(clusters, timestamp)

        item = cls._create_pose_with_status(cluster, timestamp, last_pose)
        return item

    @classmethod
    def _create_pose_with_status(
        cls, cluster: VertexCluster, timestamp: int, existing_pose: PoseVertex | None
    ) -> VertexWithStatus[PoseVertex]:
        """Creates a pose with the status.

        Args:
            cluster: a cluster for the pose.

            timestamp: a timestamp for the pose.

            existing_pose: an existing pose (optional).

        Returns:
            a pose with the status.
        """
        pose = cluster.get_latest_vertex(PoseVertex)
        if pose:
            return VertexWithStatus(pose, cluster, timestamp)
        else:
            pose = cls._create_pose(existing_pose)
            return VertexWithStatus(pose, cluster, timestamp, is_new=True)

    @classmethod
    def _create_pose(cls, pose: PoseVertex | None) -> PoseVertex:
        """Creates a new Pose based on the given one.

        Args:
            pose: an existing pose.

        Returns:
            a new pose.
        """
        if pose:
            value = pose.value
            new_index = pose.index + 1
        else:
            value = identity4x4
            new_index = 0

        return PoseVertex(new_index, value)

    @classmethod
    def _create_edge(cls, pose: PoseVertex, measurement: PoseMeasurement) -> PriorPose:
        """Creates a new edge with prior SE(3) pose factor.

        Args:
            pose: a pose vertex.

            measurement: a measurement with the pose SE(3).

        Returns:
            a new edge.
        """
        noise = pose_block_diagonal_noise_model(
            measurement.position_noise_covariance, measurement.orientation_noise_covariance
        )
        edge = PriorPose(pose, measurement, noise)
        return edge
