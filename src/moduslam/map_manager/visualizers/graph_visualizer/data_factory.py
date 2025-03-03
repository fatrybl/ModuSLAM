from dataclasses import dataclass, field

from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.cluster import Cluster
from src.moduslam.map_manager.visualizers.graph_visualizer.connection_methods import (
    Binary,
    Unary,
    create_connection,
)
from src.moduslam.map_manager.visualizers.graph_visualizer.utils import create_cluster


@dataclass
class Data:
    """Graph data to be visualized."""

    clusters: list[Cluster] = field(default_factory=list)
    binary_connections: list[Binary] = field(default_factory=list)
    unary_connections: list[Unary] = field(default_factory=list)
    mapping: dict[VertexCluster, Cluster] = field(default_factory=dict)


def create_data(graph: Graph) -> Data:
    """Create data for visualization from vertex clusters and edges.

    Args:
        graph: a graph to create a visualizable data for.

    Returns:
        data for visualization.
    """
    storage = graph.vertex_storage
    clusters = storage.clusters

    data = Data()

    for v_cluster in clusters:
        index = len(data.clusters)
        vis_cluster = create_cluster(v_cluster, index)
        data.clusters.append(vis_cluster)
        data.mapping[v_cluster] = vis_cluster

    for edge in graph.edges:
        bin_conn = create_connection(edge, storage, data.mapping)

        if isinstance(bin_conn, Binary):
            data.binary_connections.append(bin_conn)
        elif isinstance(bin_conn, Unary):
            data.unary_connections.append(bin_conn)
        else:
            continue

    return data
