from moduslam.frontend_manager.graph.custom_vertices import Pose
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.map_manager.maps.trajectory import TrajectoryMap
from moduslam.map_manager.protocols import MapFactory


class TrajectoryMapFactory(MapFactory):

    def __init__(self, pose_type: type[Pose] = Pose):
        self._map = TrajectoryMap()
        self._pose_type = pose_type

    @property
    def map(self) -> TrajectoryMap:
        return self._map

    def create_map(self, vertex_storage: VertexStorage) -> None:
        """Creates a trajectory map from the vertex storage.

        Args:
            vertex_storage: storage of graph vertices.
        """

        vertices = vertex_storage.get_vertices(self._pose_type)
        for vertex in vertices:
            t = vertex.timestamp
            p = vertex.value
            self._map.add(t, p)
