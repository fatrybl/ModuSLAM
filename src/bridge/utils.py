from collections.abc import Iterable

from src.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from src.external.metrics.vertices_connectivity import VerticesConnectivity
from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.measurements.base import Measurement
from src.moduslam.frontend_manager.main_graph.graph import (
    Graph,
    GraphCandidate,
    GraphElement,
)


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


def get_clusters_and_leftovers(
    item: list[MeasurementCluster] | ClustersWithLeftovers,
) -> tuple[list[MeasurementCluster], list[Measurement]]:
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


def remove_unconnected_candidates(candidates: list[GraphCandidate]) -> list[GraphCandidate]:
    """Removes candidates which new vertices are not fully connected with the main
    graph.

    Args:
        candidates: candidates to remove unconnected.

    Returns:
        new list of graph candidates.
    """
    new_candidates: list[GraphCandidate] = []

    for candidate in candidates:

        all_vertices = candidate.graph.vertex_storage.vertices
        is_connected = VerticesConnectivity.compute(all_vertices, candidate.elements)

        if is_connected:
            new_candidates.append(candidate)

    return new_candidates
