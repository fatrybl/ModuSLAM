from typing import TypeVar

from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex

T = TypeVar("T", bound=Vertex)


def create_new_vertex(vertex_type: type[T], graph: Graph) -> T:
    """Creates a new vertex of the given type.

    Args:
        vertex_type: a type to create an instance of.

        graph: a main graph to use.

    Returns:
        a new vertex.
    """
    last_index = graph.vertex_storage.get_last_index(vertex_type)
    latest_pose = graph.vertex_storage.get_latest_vertex(vertex_type)
    new_index = last_index + 1

    if latest_pose:
        vertex = vertex_type(new_index, latest_pose.value)
    else:
        vertex = vertex_type(new_index)

    return vertex
