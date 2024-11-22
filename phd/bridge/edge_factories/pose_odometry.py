from phd.bridge.edge_factories.factory_protocol import EdgeFactory, VertexWithStatus
from phd.bridge.edge_factories.noise_models import pose_block_diagonal_noise_model
from phd.bridge.edge_factories.utils import get_cluster, get_new_items
from phd.measurements.processed_measurements import PoseOdometry as OdometryMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose, identity4x4
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


class Factory(EdgeFactory):

    _vertex_type = Pose

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: OdometryMeasurement,
    ) -> GraphElement:
        """Creates a new edge with SE(3) pose odometry factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a measurement to create edge(s).
        """
        start = measurement.time_range.start
        stop = measurement.time_range.stop

        vertex_i = cls._get_pose_i_with_status(graph.vertex_storage, clusters, start)
        vertex_j = cls._get_pose_j_with_status(graph.vertex_storage, clusters, stop, vertex_i)

        new_vertices = get_new_items([vertex_i, vertex_j])

        edge = cls._create_edge(vertex_i.instance, vertex_j.instance, measurement)

        element = GraphElement(edge, new_vertices)
        return element

    @classmethod
    def _get_pose_i_with_status(
        cls, storage: VertexStorage, clusters: dict[VertexCluster, TimeRange], timestamp: int
    ) -> VertexWithStatus[Pose]:
        """Gets i-th (previous) pose with status.

        Args:
            storage: a global storage with clusters.

            clusters: clusters with the time ranges.

            timestamp: a timestamp of the i-th pose.

        Returns:
            a vertex with the status.
        """

        cluster = storage.get_cluster(timestamp)
        if cluster:
            item = cls._create_pose_i_with_status(storage, cluster, timestamp)
            return item

        cluster = get_cluster(clusters, timestamp)
        if cluster:
            item = cls._create_pose_i_with_status(storage, cluster, timestamp)
            return item

        else:
            cluster = VertexCluster()
            pose = cls._create_pose_i(storage)
            return VertexWithStatus(pose, cluster=cluster, is_new=True, timestamp=timestamp)

    @classmethod
    def _get_pose_j_with_status(
        cls,
        storage: VertexStorage,
        clusters: dict[VertexCluster, TimeRange],
        timestamp: int,
        vertex_i: VertexWithStatus[Pose],
    ) -> VertexWithStatus[Pose]:
        """Gets the j-th (current) pose.

        Args:
            storage: a global storage with clusters.

            clusters: current clusters.

            timestamp: a timestamp.

            vertex_i: a vertex with the status of the i-th pose.
        """
        old_cluster = storage.get_cluster(timestamp)
        if old_cluster:
            cluster = old_cluster
        else:
            cluster = get_cluster(clusters, timestamp)

        vertex_j = cls._create_pose_j_with_status(storage, cluster, timestamp, vertex_i)
        return vertex_j

    @classmethod
    def _create_pose_i(cls, storage: VertexStorage) -> Pose:
        """Creates new pose based on the latest pose in the storage.

        Args:
            storage: a storage with poses.

        Returns:
            a new pose.
        """
        latest_pose = storage.get_latest_vertex(Pose)

        if latest_pose:
            value = latest_pose.value
            index = latest_pose.index + 1
        else:
            value = identity4x4
            index = 0

        return Pose(index, value)

    @classmethod
    def _create_pose_j(cls, pose_i: VertexWithStatus[Pose], storage: VertexStorage) -> Pose:
        """Creates a new j-th pose.

        Args:
            pose_i: a vertex with the status of the i-th pose.

            storage: a storage with vertices.

        Returns:
            a new pose.
        """
        if pose_i.is_new:
            new_idx = pose_i.instance.index + 1
        else:
            last_idx = storage.get_last_index(Pose)
            new_idx = last_idx + 1

        pose = storage.get_latest_vertex(Pose)
        if pose:
            value = pose.value
        else:
            value = identity4x4

        pose = Pose(new_idx, value)
        return pose

    @classmethod
    def _create_pose_i_with_status(
        cls, storage: VertexStorage, cluster: VertexCluster, timestamp: int
    ) -> VertexWithStatus[Pose]:
        """Creates a new vertex with the status.

        Args:
            storage: a global storage with poses.

            cluster: a cluster to find an existing pose in.

            timestamp: a timestamp.

        Returns:
            a vertex with the status.
        """
        pose = cluster.get_latest_vertex(Pose)
        if pose:
            return VertexWithStatus(pose, cluster, timestamp)
        else:
            pose = cls._create_pose_i(storage)
            return VertexWithStatus(pose, cluster, is_new=True, timestamp=timestamp)

    @classmethod
    def _create_pose_j_with_status(
        cls,
        storage: VertexStorage,
        cluster: VertexCluster,
        timestamp: int,
        vertex_i: VertexWithStatus,
    ) -> VertexWithStatus[Pose]:
        """Creates a vertex with the status of the j-th pose.

        Args:
            storage: a global storage with poses.

            cluster: a cluster to find an existing pose in.

            timestamp: a timestamp.

            vertex_i: a vertex with the status of the i-th pose.

        Returns:
            a vertex with the status.
        """
        pose = cluster.get_latest_vertex(Pose)
        if pose:
            return VertexWithStatus(pose, cluster, timestamp)
        else:
            new_pose = cls._create_pose_j(vertex_i, storage)
            return VertexWithStatus(new_pose, cluster, is_new=True, timestamp=timestamp)

    @classmethod
    def _create_edge(
        cls, pose_i: Pose, pose_j: Pose, measurement: OdometryMeasurement
    ) -> PoseOdometry:
        """Creates a PoseOdometry edge.

        Args:
            pose_i: initial pose vertex.

            pose_j: final pose vertex.

            measurement: odometry measurement.

        Returns:
            new PoseOdometry edge.
        """

        noise = pose_block_diagonal_noise_model(
            measurement.position_covariance, measurement.orientation_covariance
        )
        edge = PoseOdometry(pose_i, pose_j, measurement, noise)
        return edge
