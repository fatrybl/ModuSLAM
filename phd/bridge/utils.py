from collections.abc import Iterable

from phd.bridge.objects.auxiliary_dataclasses import ClustersWithLeftovers
from phd.bridge.objects.measurements_cluster import Cluster
from phd.measurements.processed_measurements import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement


def add_elements_to_graph(
    graph: Graph, new_elements: GraphElement | Iterable[GraphElement]
) -> None:
    """Adds new element(s) to the graph.

    Args:
        graph: a graph to which the element(s) will be added.
        new_elements: new element(s) to be added.
    """
    if isinstance(new_elements, Iterable):
        for element in new_elements:
            graph.add_element(element)
    else:
        graph.add_element(new_elements)


def process_leftovers(
    item: list[Cluster] | ClustersWithLeftovers,
) -> tuple[list[Cluster], list[Measurement]]:
    """Returns clusters and leftovers.

    Args:
        item: list of clusters w or w/o leftovers.

    Returns:
        clusters, leftovers
    """
    if isinstance(item, ClustersWithLeftovers):
        return item.clusters, item.leftovers
    else:
        return item, []
