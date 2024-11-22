from collections.abc import Iterable
from typing import Any, TypeVar

from phd.bridge.edge_factories.factory_protocol import VertexWithStatus
from phd.moduslam.frontend_manager.main_graph.graph import VerticesTable
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.exceptions import ItemNotFoundError

V = TypeVar("V", bound=Vertex)


def get_new_items(items: Iterable[VertexWithStatus]) -> VerticesTable:
    """Gets new vertices with the corresponding timestamps and the clusters.

    Args:
        items: vertices with statuses.

    Returns:
        a table of clusters with the corresponding lists of new vertices with timestamps.
    """
    table: VerticesTable = {}
    for item in items:
        if item.is_new:
            vertex_with_timestamp = (item.instance, item.timestamp)
            table.update({item.cluster: [vertex_with_timestamp]})
    return table


def get_cluster(clusters: dict[VertexCluster, TimeRange], timestamp: int) -> VertexCluster:
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

    raise ItemNotFoundError("No cluster has been found for the given timestamp.")


def get_closest_cluster(
    storage: VertexStorage, timestamp: int, threshold: float
) -> VertexCluster | None:
    """Gets the closest cluster for the given timestamp and threshold.

    Args:
        storage: a storage with clusters.

        timestamp: a timestamp.

        threshold: a threshold in seconds for the distance between timestamps.
    """
    raise NotImplementedError


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
    latest_vertex = storage.get_latest_vertex(vertex_type)
    last_index = storage.get_last_index(vertex_type)

    value = latest_vertex.value if latest_vertex else default_value
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
    vertex = cluster.get_latest_vertex(vertex_type)
    if vertex:
        return VertexWithStatus(vertex, cluster, timestamp)
    else:
        vertex = create_vertex(vertex_type, storage, default_value)
        return VertexWithStatus(vertex, cluster, is_new=True, timestamp=timestamp)


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
    vertex = cluster.get_latest_vertex(v_type)
    if vertex:
        return VertexWithStatus(vertex, cluster, timestamp)
    else:
        new_vertex = create_vertex_from_previous(storage, vertex_i)
        return VertexWithStatus(new_vertex, cluster, is_new=True, timestamp=timestamp)
