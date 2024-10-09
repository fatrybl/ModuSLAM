"""Common methods for edge factories."""

from moduslam.frontend_manager.graph.base_vertices import BaseVertex
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.utils.auxiliary_methods import equal_integers


def get_last_vertex(
    vertex_type: type[BaseVertex],
    storage: VertexStorage,
    timestamp: int,
    time_margin: int,
) -> BaseVertex | None:
    """Gets the latest vertex in the storage by timestamp.

    Args:
        vertex_type: type of the vertex.

        storage: storage of vertices.

        timestamp: timestamp of the vertex.

        time_margin: time margin for searching the closest vertex.

    Returns:
        vertex if found.
    """

    vertex = storage.get_last_vertex(vertex_type)

    if vertex and equal_integers(vertex.timestamp, timestamp, time_margin):
        return vertex
    else:
        return None
