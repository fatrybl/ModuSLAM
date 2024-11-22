from collections.abc import Iterable

from phd.bridge.edge_factories.factory_protocol import VertexWithStatus
from phd.moduslam.frontend_manager.main_graph.graph import VerticesTable
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.exceptions import ItemNotFoundError


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
