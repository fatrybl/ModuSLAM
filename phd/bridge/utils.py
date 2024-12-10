from collections.abc import Iterable

from phd.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from phd.external.metrics.candidate_connectivity import (
    check_connectivity,
    get_old_vertices,
)
from phd.measurement_storage.cluster import Cluster
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import (
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

        edges = [element.edge for element in candidate.elements]
        new_vertices = {
            new_vertex.instance
            for element in candidate.elements
            for new_vertex in element.new_vertices
        }
        old_vertices = get_old_vertices(candidate.graph, new_vertices)

        is_connected = check_connectivity(edges, old_vertices, new_vertices)

        if is_connected:
            new_candidates.append(candidate)

    return new_candidates
