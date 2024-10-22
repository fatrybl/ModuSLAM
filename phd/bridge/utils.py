from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from phd.bridge.edges_builder.distributor import distribute
from phd.bridge.objects.graph_candidate import VertexCluster
from phd.external.objects.auxiliary_objects import ClustersWithLeftovers
from phd.external.objects.measurements import Measurement
from phd.external.objects.measurements_cluster import Cluster
from phd.moduslam.frontend_manager.graph.graph import Graph


def create_edges_and_vertices(
    measurement: Measurement, graph: Graph, vertices_db: list[VertexCluster]
) -> tuple[list[Edge], list[Vertex]]:
    """Creates edges for the given measurement.

    Args:
        measurement: measurement to create edges from.

        graph: graph to create edges for.

        vertices_db: database with new vertices.

    Returns:
        new edges and vertices.
    """
    edge_factory = distribute(measurement)
    edges, vertices = edge_factory.create(measurement, graph, vertices_db)
    return edges, vertices


def process_leftovers(
    item: list[Cluster] | ClustersWithLeftovers, leftovers_db: list[Measurement]
) -> list[Cluster]:
    """Adds leftovers (if exist) to the database and returns clusters.

    Args:
        item: clusters w or w/o leftovers.

        leftovers_db: database with leftovers.

    Returns:
        clusters.
    """
    if isinstance(item, list):
        return item
    else:
        leftovers_db.extend(item.leftovers)
        return item.clusters


def solve(graph: Graph) -> float:
    """Solve the problem with the given graph."""
    raise NotImplementedError
