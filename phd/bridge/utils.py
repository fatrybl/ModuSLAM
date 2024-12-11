from collections.abc import Iterable

from phd.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from phd.external.metrics.vertices_connectivity import check_connectivity
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import (
    Graph,
    GraphCandidate,
    GraphElement,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex


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


def get_old_vertices(graph: Graph, new_vertices: set[Vertex]) -> set[Vertex]:
    """Gets vertices of the graph which are not in new vertices.

    Args:
        graph: a graph to get vertices from.

        new_vertices: new vertices to find the old ones.

    Returns:
        old vertices.
    """
    all_vertices = set(graph.connections.keys())
    return all_vertices - new_vertices


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
