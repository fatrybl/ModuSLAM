from collections.abc import Iterable

from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from phd.bridge.edges_builder.distributor import distribute
from phd.bridge.objects.search_database import Database
from phd.bridge.objects.vertices_cluster import Cluster as VerticesCluster
from phd.external.objects.auxiliary_objects import ClustersWithLeftovers
from phd.external.objects.measurements import Measurement
from phd.external.objects.measurements_cluster import Cluster as MeasurementCluster
from phd.moduslam.frontend_manager.graph.graph import Graph


def create_edges_and_vertices(
    measurement: Measurement, database: Database
) -> tuple[list[Edge], list[Vertex]]:
    """Creates edges for the given measurement.

    Args:
        measurement: measurement to create edges from.

        database: database to search vertices in.

    Returns:
        new edges and vertices.
    """
    edge_factory = distribute(measurement)
    edges, vertices = edge_factory.create(measurement, database)
    return edges, vertices


def process_leftovers(
    item: list[MeasurementCluster] | ClustersWithLeftovers, leftovers_db: list[Measurement]
) -> list[MeasurementCluster]:
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


def change_vertices(edges: Iterable[Edge], cluster: VerticesCluster) -> None:
    """Changes the vertices of the given edge."""
    raise NotImplementedError
