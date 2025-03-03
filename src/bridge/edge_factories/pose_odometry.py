from src.bridge.edge_factories.factory_protocol import EdgeFactory, VertexWithStatus
from src.bridge.edge_factories.utils import (
    create_new_vertices,
    create_vertex,
    create_vertex_i_with_status,
    create_vertex_j_with_status,
    get_cluster_for_timestamp_from_dict,
)
from src.measurement_storage.measurements.pose_odometry import (
    Odometry as OdometryMeasurement,
)
from src.moduslam.frontend_manager.main_graph.edges.noise_models import (
    huber_diagonal_noise_model,
)
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose, identity4x4
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.exceptions import LoopError


class Factory(EdgeFactory):

    _vertex_type = Pose

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: OdometryMeasurement,
    ) -> GraphElement[PoseOdometry]:
        """Creates a new edge with SE(3) pose odometry factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a measurement to create edge(s).

        Returns:
            graph element with pose odometry edge.

        Raises:
            LoopError: if pose_i is equal to pose_j
        """
        start = measurement.time_range.start
        stop = measurement.time_range.stop

        pose_i = cls._get_pose_i_with_status(graph.vertex_storage, clusters, start)
        pose_j = cls._get_pose_j_with_status(graph.vertex_storage, clusters, stop, pose_i)

        if pose_i is pose_j:
            raise LoopError("pose_i is equal to pose_j")

        new_vertices = create_new_vertices([pose_i, pose_j])

        edge = cls._create_edge(pose_i.instance, pose_j.instance, measurement)

        return GraphElement(edge, {pose_i.instance: start, pose_j.instance: stop}, new_vertices)

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
            item = create_vertex_i_with_status(Pose, storage, cluster, timestamp, identity4x4)
            return item

        cluster = get_cluster_for_timestamp_from_dict(clusters, timestamp)
        if cluster:
            item = create_vertex_i_with_status(Pose, storage, cluster, timestamp, identity4x4)
            return item

        cluster = VertexCluster()
        pose = create_vertex(Pose, storage, identity4x4)
        return VertexWithStatus(pose, cluster, timestamp, is_new=True)

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
        cluster = storage.get_cluster(timestamp)
        if cluster:
            item = create_vertex_j_with_status(storage, cluster, timestamp, vertex_i)
            return item

        cluster = get_cluster_for_timestamp_from_dict(clusters, timestamp)
        if cluster:
            item = create_vertex_j_with_status(storage, cluster, timestamp, vertex_i)
            return item

        cluster = VertexCluster()
        pose = create_vertex(Pose, storage, identity4x4)
        return VertexWithStatus(pose, cluster, timestamp, is_new=True)

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
        huber_loss_trh = 0.5

        trans_cov = measurement.position_covariance
        rot_cov = measurement.orientation_covariance

        variance = (
            rot_cov[0][0],
            rot_cov[1][1],
            rot_cov[2][2],
            trans_cov[0][0],
            trans_cov[1][1],
            trans_cov[2][2],
        )

        noise = huber_diagonal_noise_model(variance, huber_loss_trh)
        return PoseOdometry(pose_i, pose_j, measurement, noise)
