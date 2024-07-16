from moduslam.frontend_manager.graph.custom_vertices import CameraPose
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.map_manager.maps.trajectory import TrajectoryMap


class TrajectoryMapFactory:

    def __init__(self):
        self._map = TrajectoryMap()
        self._vertex_type = CameraPose

    @property
    def map(self) -> TrajectoryMap:
        return self._map

    def create(self, vertex_storage: VertexStorage):
        """Creates a trajectory map from the vertex storage."""

        vertices = vertex_storage.get_vertices(self._vertex_type)
        for vertex in vertices:
            t = vertex.timestamp
            p = vertex.value
            self._map.add(t, p)
