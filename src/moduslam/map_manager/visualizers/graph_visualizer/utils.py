from collections.abc import Iterable

import numpy as np

from src.custom_types.numpy import VectorN
from src.measurement_storage.measurements.base import Measurement, TimeRangeMeasurement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.cluster import (
    Cluster,
    Vertex,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.connection_objects import (
    Binary,
    Unary,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.mappings import (
    vertex_encodings,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.visualizer_params import (
    BinaryConnectionParams,
)
from src.utils.auxiliary_dataclasses import Position2D
from src.utils.exceptions import ItemNotExistsError


def get_clusters_for_binary_connections(
    measurement: TimeRangeMeasurement, storage: VertexStorage, mapping: dict[VertexCluster, Cluster]
) -> tuple[Cluster, Cluster]:
    """Gets clusters for the binary connection.

    Args:
        measurement: a TimeRangeMeasurement edge.

        storage: a vertex storage.

        mapping: a mapping table from vertex clusters to visualizable clusters.

    Returns:
        1-st and 2-nd clusters.

    Raises:
        ItemNotExistsError: if vertex clusters not found for timestamps.
    """
    t_range = measurement.time_range
    t1, t2 = t_range.start, t_range.stop

    v_cluster1 = storage.get_cluster(t1)
    v_cluster2 = storage.get_cluster(t2)

    if v_cluster1:
        cls1 = mapping[v_cluster1]
    else:
        raise ItemNotExistsError(f"Vertex clusters not found for timestamp {t1}.")

    if v_cluster2:
        cls2 = mapping[v_cluster2]
    else:
        raise ItemNotExistsError(f"Vertex clusters not found for timestamp {t2}.")

    return cls1, cls2


def get_cluster_for_unary_connection(
    measurement: Measurement, storage: VertexStorage, mapping: dict[VertexCluster, Cluster]
) -> Cluster:
    """Gets cluster for the unary connection.

    Args:
        measurement: a measurement.

        storage: a vertex storage.

        mapping: a mapping table from vertex clusters to visualizable clusters.

    Returns:
        cluster for the unary connection.

    Raises:
        ItemNotExistsError: if vertex clusters not found for timestamps.
    """
    t = measurement.timestamp

    v_cluster = storage.get_cluster(t)

    if v_cluster:
        cls = mapping[v_cluster]
    else:
        raise ItemNotExistsError(f"Vertex clusters not found for timestamp {t}.")

    return cls


def create_cluster(vertex_cluster: VertexCluster, index: int) -> Cluster:
    """Create a cluster for visualization.

    Args:
        vertex_cluster: a vertex cluster.

        index: a cluster ID.

    Returns:
        a cluster for visualization.
    """
    vertices = vertex_cluster.vertices
    cluster = Cluster(index, vertex_cluster.time_range)

    for vertex in vertices:
        label = vertex_encodings[type(vertex)] + str(index)
        new = Vertex(vertex.index, label)
        cluster.add(new)

    return cluster


def calculate_vertical_line_properties(
    connections: Iterable[Unary],
) -> dict[Cluster, list[float]]:
    """Calculate properties for drawing vertical lines for each cluster.

    Args:
        connections: Unary connections for clusters.

    Returns:
        A dictionary mapping each cluster to a list of heights for its vertical lines.
    """
    cluster_heights: dict[Cluster, list[float]] = {}

    for connection in connections:
        cluster = connection.source
        if cluster not in cluster_heights:
            cluster_heights[cluster] = []

        cluster_heights[cluster].append(len(cluster_heights[cluster]) + 1)

    return cluster_heights


def calculate_curve_properties(
    connection: Binary,
    connection_counts: dict[tuple[Cluster, Cluster], int],
    vis_params: BinaryConnectionParams,
) -> tuple[Position2D, Position2D, Position2D]:
    """Calculate properties for drawing a Bézier curve between two clusters.

    Args:
        connection: The connection between two clusters.
        connection_counts: A dictionary tracking the number of connections between clusters.
        vis_params: Visualization parameters.

    Returns:
        start point, stop point, middle point
    """
    cls1, cls2 = connection.source, connection.target
    key = (cls1, cls2) if cls1.top_center.x < cls2.top_center.x else (cls2, cls1)

    if key not in connection_counts:
        connection_counts[key] = 0
    connection_counts[key] += 1

    dynamic_offset = vis_params.base_offset * ((connection_counts[key] + 1) // 2)
    if connection_counts[key] % 2 == 0:
        dynamic_offset *= -1

    pos1, pos2 = cls1.top_center, cls2.top_center
    mid_x = (pos1.x + pos2.x) / 2
    mid_y = (pos1.y + pos2.y) / 2 + abs(pos2.x - pos1.x) * (0.3 + dynamic_offset)

    return pos1, pos2, Position2D(mid_x, mid_y)


def generate_bezier_curve(
    point1: Position2D, point2: Position2D, mid_point: Position2D, curvature: float = 0.2
) -> tuple[VectorN, VectorN]:
    """Generate a Bézier curve between two points with adjustable curvature.

    Args:
        point1: start point.

        point2: end point.

        mid_point: middle point.

        curvature: factor to adjust the curvature of the curve.

    Returns:
        x, y coordinates of the curve.
    """
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    mid_x, mid_y = mid_point.x, mid_point.y

    mid_y += abs(x2 - x1) * curvature

    t = np.linspace(0, 1, 100)
    curve_x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * mid_x + t**2 * x2
    curve_y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * mid_y + t**2 * y2

    return curve_x, curve_y
