from typing import Callable, Iterable

import gtsam
from gtsam import NavState, Pose3, Pose3Vector, Rot3

from slam.frontend_manager.graph.vertices import GraphVertex, GtsamVertex


class GtsamVertexUpdater:
    """Updates vertices of the Graph based on GTSAM inner methods."""

    def __init__(self, values: gtsam.Values) -> None:
        self._table: dict[type[GtsamVertex], Callable] = {
            Rot3: values.atRot3,
            Pose3Vector: values.atVector,
            Pose3: values.atPose3,
            NavState: values.atNavState,
        }

    def update(self, vertices: Iterable[GraphVertex]) -> None:
        """Updates vertices of the graph."""
        for vertex in vertices:
            base_vertex_type = type(vertex.base_vertex)
            update_method = self._table[base_vertex_type]
            new_values = update_method(vertex.gtsam_index)
            vertex.update(new_values)
