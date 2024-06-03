from collections import defaultdict

from moduslam.data_manager.factory.element import Element
from moduslam.frontend_manager.graph.custom_edges import VisualOdometry
from moduslam.frontend_manager.graph.custom_vertices import CameraPose
from moduslam.utils.deque_set import DequeSet


def create_vertex_elements_table(
    vertices: DequeSet[CameraPose], edges: set[VisualOdometry]
) -> dict[CameraPose, set[Element]]:
    """Creates "CameraPose -> elements" table.

    Args:
        vertices: vertices to get elements for.

        edges: edges to check.

    Returns:
        "vertex -> elements" table.
    """

    table: dict[CameraPose, set[Element]] = defaultdict(set)

    num_poses = len(vertices)

    for i, vertex in enumerate(vertices):
        if i == num_poses - 1:
            for e in vertex.edges:
                if isinstance(e, VisualOdometry):
                    m = e.measurements[0]
                    element = m.elements[1]
                    table[vertex].add(element)
        else:
            for e in vertex.edges:
                if e in edges and isinstance(e, VisualOdometry):
                    m = e.measurements[0]
                    element = m.elements[0]
                    table[vertex].add(element)
                    edges.remove(e)
    return table
