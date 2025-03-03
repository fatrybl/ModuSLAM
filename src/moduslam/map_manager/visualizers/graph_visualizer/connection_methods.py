from collections.abc import Callable

from src.moduslam.frontend_manager.main_graph.edges.base import Edge
from src.moduslam.frontend_manager.main_graph.edges.combined_imu_odometry import (
    ImuOdometry,
)
from src.moduslam.frontend_manager.main_graph.edges.gps_position import GpsPosition
from src.moduslam.frontend_manager.main_graph.edges.linear_velocity import (
    LinearVelocity,
)
from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.cluster import Cluster
from src.moduslam.map_manager.visualizers.graph_visualizer.connection_objects import (
    Binary,
    Unary,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.mappings import (
    edge_encodings,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.utils import (
    get_cluster_for_unary_connection,
    get_clusters_for_binary_connections,
)


def get_label(edge: Edge) -> str:
    """Get label for the edge.

    Args:
        edge: an edge to get a label for.

    Returns:
        a label.
    """
    encoding = edge_encodings[type(edge)]
    index_str = str(edge.index)
    return encoding + " " + index_str


def create_connection(
    edge: Edge, storage: VertexStorage, mapping: dict[VertexCluster, Cluster]
) -> Binary | Unary | None:
    """Create a connection for visualization.

    Args:
        edge: an edge to create a connection for.

        storage: a vertex storage.

        mapping: a mapping between vertex clusters and visualizable clusters.
    """
    method = edge_type_method_table[type(edge)]
    conn = method(edge, storage, mapping)
    return conn


def pose_odometry_connection(
    edge: PoseOdometry, storage: VertexStorage, mapping: dict[VertexCluster, Cluster]
) -> Binary:
    """Create binary connection for PoseOdometry edge.

    Args:
        edge: a PoseOdometry edge.

        storage: a vertex storage.

        mapping: a mapping table from vertex clusters to visualizable clusters.

    Returns:
        a binary connection.

    Raises:
        ItemNotExistsError: if vertex clusters not found for timestamps.
    """
    cls1, cls2 = get_clusters_for_binary_connections(edge.measurement, storage, mapping)

    label = get_label(edge)

    return Binary(cls1, cls2, label)


def imu_odometry_connection(
    edge: ImuOdometry, storage: VertexStorage, mapping: dict[VertexCluster, Cluster]
) -> Binary:
    """Create binary connection for ImuOdometry edge.

    Args:
        edge: an ImuOdometry edge.

        storage: a vertex storage.

        mapping: a mapping table from vertex clusters to visualizable clusters.

    Returns:
        a binary connection.

    Raises:
        ItemNotExistsError: if vertex clusters not found for timestamps.
    """
    cls1, cls2 = get_clusters_for_binary_connections(edge.measurement, storage, mapping)

    label = get_label(edge)

    return Binary(cls1, cls2, label, draw_below=True)


def gps_connection(
    edge: GpsPosition, storage: VertexStorage, mapping: dict[VertexCluster, Cluster]
) -> Unary:
    """Create unary connection for GpsPosition edge.

    Args:
        edge: a GpsPosition edge.

        storage: a vertex storage.

        mapping: a mapping table from vertex clusters to visualizable clusters.

    Returns:
        a unary connection.

    Raises:
        ItemNotExistsError: if vertex clusters not found for timestamps.
    """

    cluster = get_cluster_for_unary_connection(edge.measurement, storage, mapping)

    label = get_label(edge)

    return Unary(cluster, label)


def pose_connection(
    edge: PriorPose, storage: VertexStorage, mapping: dict[VertexCluster, Cluster]
) -> Unary:
    """Create unary connection for Pose edge.

    Args:
        edge: a Pose edge.

        storage: a vertex storage.

        mapping: a mapping table from vertex clusters to visualizable clusters.

    Returns:
        a unary connection.

    Raises:
        ItemNotExistsError: if vertex clusters not found for timestamps.
    """
    cluster = get_cluster_for_unary_connection(edge.measurement, storage, mapping)

    label = get_label(edge)

    return Unary(cluster, label)


def velocity_connection(
    edge: LinearVelocity, storage: VertexStorage, mapping: dict[VertexCluster, Cluster]
) -> Unary:
    """Create unary connection for Velocity edge.

    Args:
        edge: a Velocity edge.

        storage: a vertex storage.

        mapping: a mapping table from vertex clusters to visualizable clusters.

    Returns:
        a unary connection.

    Raises:
        ItemNotExistsError: if vertex clusters not found for timestamps.
    """
    cluster = get_cluster_for_unary_connection(edge.measurement, storage, mapping)

    label = get_label(edge)

    return Unary(cluster, label)


"""Mapping between edge types and methods to create connections between visualizable clusters."""

edge_type_method_table: dict[type[Edge], Callable] = {
    PoseOdometry: pose_odometry_connection,
    ImuOdometry: imu_odometry_connection,
    GpsPosition: gps_connection,
    PriorPose: pose_connection,
    LinearVelocity: velocity_connection,
}
