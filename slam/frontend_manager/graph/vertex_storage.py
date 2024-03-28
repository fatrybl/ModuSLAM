import logging
from collections.abc import Iterable
from typing import Generic, overload

import gtsam
from plum import dispatch

from slam.frontend_manager.graph.index_generator import IndexStorage
from slam.frontend_manager.graph.vertices import (
    CameraFeature,
    CameraPose,
    GraphVertex,
    ImuBias,
    LidarPose,
    NavState,
    Pose,
    Velocity,
    Vertex,
)
from slam.utils.deque_set import DequeSet
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class VertexStorage(Generic[GraphVertex]):
    """Stores vertices of the Graph.

    TODO:
        maybe get_vertcies(type) to get all vertices of the graph of the given type ?
    """

    def __init__(self):
        self.vertices = DequeSet[GraphVertex]()
        self.index_storage = IndexStorage()

        self._optimizable_vertices = OrderedSet[GraphVertex]()
        self._constant_vertices = OrderedSet[GraphVertex]()

        self._table: dict[type[Vertex], DequeSet] = {
            Pose: DequeSet[Pose](),
            Velocity: DequeSet[Velocity](),
            NavState: DequeSet[NavState](),
            ImuBias: DequeSet[ImuBias](),
            CameraPose: DequeSet[CameraPose](),
            LidarPose: DequeSet[LidarPose](),
            CameraFeature: DequeSet[CameraFeature](),
        }

    @property
    def optimizable_vertices(self) -> OrderedSet[GraphVertex]:
        """Optimizable vertices in the Graph.

        Returns:
            (DequeSet[GraphVertex]): optimizable vertices in the graph.
        """
        return self._optimizable_vertices

    @property
    def constant_vertices(self) -> OrderedSet[GraphVertex]:
        """Constant vertices in the Graph.

        Returns:
            (DequeSet[GraphVertex]): constant vertices in the graph.
        """
        return self._constant_vertices

    def get_vertices(self, vertex_type: type[Vertex]) -> DequeSet:
        """Returns vertices of the given type.

        Args:
            vertex_type (type[GraphVertex]): type of the vertices.

        Returns:
            (DequeSet): vertices of the given type.
        """
        return self._table[vertex_type]

    @property
    def pose(self) -> DequeSet[Pose]:
        """Pose vertex in the Graph.

        Position and orientation (SE3).
        Returns:
            (DequeSet[Pose]): poses in the graph.
        """
        return self._table[Pose]

    @property
    def velocity(self) -> DequeSet[Velocity]:
        """Linear velocity vertex in Graph.

        Returns:
            (DequeSet[Velocity]): linear velocity in the graph.
        """
        return self._table[Velocity]

    @property
    def nav_state(self) -> DequeSet[NavState]:
        """Navigation state vertex in Graph.

        Returns:
            (DequeSet[NavState]): navigation state in the graph.
        """
        return self._table[NavState]

    @property
    def imu_bias(self) -> DequeSet[ImuBias]:
        """IMU bias vertex in Graph.

        Returns:
            (DequeSet[ImuBias]): IMU bias in the graph.
        """
        return self._table[ImuBias]

    @property
    def camera_pose(self) -> DequeSet[CameraPose]:
        """The pose where an image has been taken.

        Returns:
            (DequeSet[CameraPose]): camera pose in the graph.
        """
        return self._table[CameraPose]

    @property
    def lidar_pose(self) -> DequeSet[LidarPose]:
        """The pose where a point-cloud has been registered.

        Returns:
            (DequeSet[LidarPose]): lidar pose in the graph.
        """
        return self._table[LidarPose]

    @property
    def camera_feature(self) -> DequeSet[CameraFeature]:
        """Camera feature based landmark in the Graph.

        Returns:
            (DequeSet[CameraFeature]): camera feature in the graph.
        """
        return self._table[CameraFeature]

    @overload
    def add(self, vertex: GraphVertex) -> None:
        """
        @overload.
        Adds new vertex based on its type.
        Args:
            vertex (GraphVertex): new vertex to be added to the graph.
        """
        t = type(vertex)
        self.index_storage.add(vertex.index)
        self.vertices.add(vertex)
        self._table[t].add(vertex)
        if vertex.optimizable:
            self._optimizable_vertices.add(vertex)
        else:
            self._constant_vertices.add(vertex)

    @overload
    def add(self, vertices: Iterable[GraphVertex]) -> None:
        """
        @overload.
        Adds new vertices to collections based on its type.
        Args:
            vertices (Iterable[GraphVertex]): new vertices to be added to the graph.
        """
        [self.add(v) for v in vertices]

    @dispatch
    def add(self, vertex=None):
        """
        @overload.

        Adds new vertex(s) to the graph.

        Calls:
            1.  add single vertex to the graph.
                Args:
                    vertex (GraphVertex): new vertex to be added to the graph.

            2.  add multiple vertices to the graph.
                Args:
                    vertices (Iterable[GraphVertex]): new vertices to be added to the graph.
        """

    @overload
    def remove(self, vertex: GraphVertex) -> None:
        """
        @overload.
        Removes vertex from the graph.
        Args:
            vertex (GraphVertex): a vertex to be removed from the graph.
        """
        t = type(vertex)
        self.index_storage.remove(vertex.index)
        self.vertices.remove(vertex)
        self._table[t].remove(vertex)
        if vertex.optimizable:
            self._optimizable_vertices.remove(vertex)
        else:
            self._constant_vertices.remove(vertex)

    @overload
    def remove(self, vertices: Iterable[GraphVertex]) -> None:
        """
        @overload.
        Removes multiple vertices from the graph.
        Args:
            vertices (Iterable[GraphVertex]): vertices to be removed from the graph.
        """
        [self.remove(v) for v in vertices]

    @dispatch
    def remove(self, vertex=None):
        """
        @overload.

        Removes vertex(s) from the graph.

        Calls:
            1.  remove single vertex from the graph.
                Args:
                    vertex (GraphVertex): a vertex to be removed from the graph.

            2.  remove multiple vertices from the graph.
                Args:
                    vertices (Iterable[GraphVertex]): vertices to be removed from the graph.
        """

    def update(self, new_values: gtsam.Values) -> None:
        """Updates the vertices with new values.

        Args:
            new_values (gtsam.Values): new values for vertices.
        """

        [vertex.update(new_values) for vertex in self._optimizable_vertices]
        [vertex.update() for vertex in self._constant_vertices]

    @staticmethod
    def find_closest_vertex(
        vertex_type: type[GraphVertex], timestamp: int, margin: int
    ) -> GraphVertex | None:
        """Finds the closest vertex with the given timestamp, time margin and type.

        algorithm:
            1.  from vertices storage get all ve.
            2.  if not found, find the closest vertex with the given time margin.

        Args:
            vertex_type (type[GraphVertex): type of vertex to find.
            timestamp (int): timestamp to compare with.
            margin (int): margin for the search.

        Returns:
            (GraphVertex | None): closest vertex if found, None otherwise.
        """
        return None

    def get_last_vertex(self, vertex_type: type[GraphVertex]) -> GraphVertex | None:
        """
        Gets the previous vertex from the graph.
        Args:
            vertex_type (type[GraphVertex]): type of the vertex to find.

        Returns:
            (GraphVertex): previous vertex.
        """
        msg = f"No previous vertex of type {vertex_type!r} found."
        try:
            v = self.get_vertices(vertex_type)[-1]
            return v
        except IndexError:
            logger.info(msg)
            return None
        except KeyError:
            logger.info(msg)
            return None
