from phd.bridge.edges_builder.distributor import distribute
from phd.external.objects.auxiliary_objects import ClustersWithLeftovers
from phd.external.objects.measurements import Measurement
from phd.external.objects.measurements_cluster import Cluster as MeasurementCluster
from phd.moduslam.frontend_manager.main_graph.element import GraphElement
from phd.moduslam.frontend_manager.main_graph.graph import Graph


def create_graph_elements(measurement: Measurement, graph: Graph) -> list[GraphElement]:
    """Creates graph elements for the given measurement.

    Args:
        measurement: a measurement to create edges from.

        graph: the graph to create elements for.

    Returns:
        new graph elements.
    """
    edge_factory = distribute(measurement)
    new_elements = edge_factory.create(measurement, graph)
    return new_elements


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
