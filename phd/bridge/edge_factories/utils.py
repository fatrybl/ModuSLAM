from collections.abc import Iterable
from typing import Any, TypeVar

from phd.bridge.edge_factories.factory_protocol import VertexWithStatus
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange

V = TypeVar("V", bound=Vertex)


def create_new_vertices(vertices: Iterable[VertexWithStatus]) -> list[NewVertex]:
    """Creates new vertices based on the status of the given ones.

    Args:
        vertices: vertices with statuses.

    Returns:
        a table of clusters with the corresponding lists of new vertices with timestamps.
    """
    new_vertices: list[NewVertex] = []

    for item in vertices:
        if item.is_new:
            vertex = NewVertex(item.instance, item.cluster, item.timestamp)
            new_vertices.append(vertex)

    return new_vertices


def get_cluster_for_timestamp(
    clusters: dict[VertexCluster, TimeRange], timestamp: int
) -> VertexCluster | None:
    """Gets the cluster which time range includes the given timestamp.

    Args:
        clusters: clusters to find in.

        timestamp: a timestamp of the cluster.

    Returns:
        a cluster containing the timestamp.

    Raises:
        ItemNotFoundError: if no cluster has been found for the given timestamp.
    """
    for cluster, time_range in clusters.items():
        if time_range.start <= timestamp <= time_range.stop:
            return cluster

    return None


def get_cluster(
    storage: VertexStorage, clusters: dict[VertexCluster, TimeRange], timestamp: int
) -> VertexCluster:
    """Finds a cluster in the storage or in clusters by timestamp.

    Args:
        storage: a storage with clusters.

        clusters: clusters to find in.

        timestamp: a timestamp of the cluster.

    Returns:
        a cluster containing the timestamp.
    """
    existing = storage.get_cluster(timestamp)
    if existing:
        return existing

    cluster = get_cluster_for_timestamp(clusters, timestamp)
    if cluster:
        return cluster

    return VertexCluster()


def get_closest_cluster(storage: VertexStorage, timestamp: int, threshold: int):
    """Gets the closest cluster for the given timestamp and threshold.

    Args:
        storage: a storage with clusters.

        timestamp: a timestamp.

        threshold: a threshold in nanoseconds for the distance between timestamps.

    Returns:
        The closest cluster if one exists within the threshold, otherwise None.
    """
    for cluster in reversed(storage.clusters):

        if abs(timestamp - cluster.time_range.stop) <= threshold:
            return cluster

        if abs(cluster.time_range.start - timestamp) <= threshold:
            return cluster

        if cluster.time_range.start <= timestamp <= cluster.time_range.stop:
            return cluster

        if abs(cluster.time_range.stop + threshold) < timestamp:
            break

    return None


def create_vertex(vertex_type: type[V], storage: VertexStorage, default_value: Any) -> V:
    """Creates new vertex based on the value of the latest vertex in the storage (if
    exists).

    Args:
        vertex_type: a type of the vertex to create.

        storage: a storage with vertices.

        default_value: a default value for the vertex.

    Returns:
        a new vertex.
    """
    last_vertex = storage.get_last_vertex(vertex_type)
    try:
        last_index = storage.get_last_index(vertex_type)
    except KeyError:
        last_index = -1

    value = last_vertex.value if last_vertex else default_value
    index = last_index + 1

    return vertex_type(index, value)


def create_vertex_from_previous(storage: VertexStorage, previous: VertexWithStatus[V]) -> V:
    """Creates a new pose based on the given pose.

    Args:
        storage: a storage with vertices.

        previous: a previous pose.

    Returns:
        a new pose.
    """
    v_type = type(previous.instance)
    if previous.is_new:
        new_idx = previous.instance.index + 1
    else:
        last_idx = storage.get_last_index(v_type)
        new_idx = last_idx + 1

    return v_type(new_idx, previous.instance.value)


def create_vertex_i_with_status(
    vertex_type: type[V],
    storage: VertexStorage,
    cluster: VertexCluster,
    timestamp: int,
    default_value: Any,
) -> VertexWithStatus[V]:
    """Creates a new vertex with the status.

    Args:
        vertex_type: a type of the vertex to create.

        storage: a storage with vertices.

        cluster: a cluster to find an existing vertex in.

        timestamp: a timestamp.

        default_value: a default value for the vertex.

    Returns:
        a new vertex with the status.
    """
    vertex = cluster.get_last_vertex(vertex_type)
    if vertex:
        return VertexWithStatus(vertex, cluster, timestamp)

    vertex = create_vertex(vertex_type, storage, default_value)
    return VertexWithStatus(vertex, cluster, timestamp, is_new=True)


def create_vertex_j_with_status(
    storage: VertexStorage,
    cluster: VertexCluster,
    timestamp: int,
    vertex_i: VertexWithStatus[V],
) -> VertexWithStatus[V]:
    """Creates a new vertex with the status.

    Args:
        storage: a storage with velocities.

        cluster: a cluster to find an existing velocity in.

        timestamp: a timestamp.

        vertex_i: a previous vertex.

    Returns:
        a new vertex with the status.
    """
    v_type = type(vertex_i.instance)
    vertex = cluster.get_last_vertex(v_type)
    if vertex:
        return VertexWithStatus(vertex, cluster, timestamp)
    else:
        new_vertex = create_vertex_from_previous(storage, vertex_i)
        return VertexWithStatus(new_vertex, cluster, timestamp, is_new=True)
