from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.map_manager.maps.trajectory import TrajectoryMap
from phd.moduslam.map_manager.protocols import MapFactory


class TrajectoryMapFactory(MapFactory):

    def __init__(self):
        self._map = TrajectoryMap()

    @property
    def map(self) -> TrajectoryMap:
        return self._map

    def create_map(self, vertex_storage: VertexStorage) -> None:
        """Creates a trajectory map from the vertex storage.

        Args:
            vertex_storage: storage of graph vertices.
        """

        # vertices = vertex_storage.get_vertices(Pose)
        raise NotImplementedError
