"""Common utility functions for edge factories."""

import gtsam

from moduslam.frontend_manager.graph.base_vertices import GraphVertex, OptimizableVertex
from moduslam.frontend_manager.graph.index_generator import generate_index
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.utils.auxiliary_methods import equal_integers


def update_vertex(source_vertex: OptimizableVertex, target_vertex: OptimizableVertex):
    """Updates the target vertex with the source vertex value.

    Args:
        source_vertex: vertex to copy the value from.

        target_vertex: vertex to copy the value to.
    """
    v = gtsam.Values()
    v.insert(target_vertex.gtsam_index, source_vertex.gtsam_instance)
    target_vertex.update(v)


def find_vertex(
    vertex_type: type[GraphVertex],
    storage: VertexStorage,
    timestamp: int,
    time_margin: int,
) -> GraphVertex | None:
    """Tries to find a vertex in the storage.

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

    vertex = storage.find_closest_optimizable_vertex(vertex_type, timestamp, time_margin)
    if vertex:
        return vertex

    return None


def get_vertex(
    vertex_type: type[GraphVertex],
    storage: VertexStorage,
    timestamp: int,
    time_margin: int,
) -> GraphVertex:
    """Find vertex or creates a new one.

    Args:
        vertex_type: type of the vertex.

        storage: storage of the vertices.

        timestamp: timestamp of the vertex.

        time_margin: time margin for the vertex search.

    Returns:
        vertex.
    """
    vertex = find_vertex(vertex_type, storage, timestamp, time_margin)

    if not vertex:
        new_index = generate_index(storage.index_storage)
        vertex = vertex_type(timestamp=timestamp, index=new_index)

    return vertex
