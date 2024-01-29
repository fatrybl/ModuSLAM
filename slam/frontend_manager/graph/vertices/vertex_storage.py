from collections.abc import Iterable
from typing import Generic

from plum import dispatch, overload

from slam.frontend_manager.graph.vertices.vertices import (
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


class VertexStorage(Generic[GraphVertex]):
    """
    Stores vertices of the Graph.
    """

    def __init__(self):
        self.vertices = DequeSet[GraphVertex]()

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
    def pose(self) -> DequeSet[Pose]:
        """
        Pose vertex in the Graph.
        Position and orientation (SE3).
        Returns:
            (DequeSet[Pose]): poses in the graph.
        """
        return self._table[Pose]

    @property
    def velocity(self) -> DequeSet[Velocity]:
        """
        Linear velocity vertex in Graph.
        Returns:
            (DequeSet[Velocity]): linear velocity in the graph.

        """
        return self._table[Velocity]

    @property
    def nav_state(self) -> DequeSet[NavState]:
        """
        Navigation state vertex in Graph.
        Returns:
            (DequeSet[NavState]): navigation state in the graph.
        """
        return self._table[NavState]

    @property
    def imu_bias(self) -> DequeSet[ImuBias]:
        """
        IMU bias vertex in Graph.
        Returns:
            (DequeSet[ImuBias]): IMU bias in the graph.
        """
        return self._table[ImuBias]

    @property
    def camera_pose(self) -> DequeSet[CameraPose]:
        """
        The pose where an image has been taken.
        Returns:
            (DequeSet[CameraPose]): camera pose in the graph.
        """
        return self._table[CameraPose]

    @property
    def lidar_pose(self) -> DequeSet[LidarPose]:
        """
        The pose where a point-cloud has been registered.
        Returns:
            (DequeSet[LidarPose]): lidar pose in the graph.
        """
        return self._table[LidarPose]

    @property
    def camera_feature(self) -> DequeSet[CameraFeature]:
        """
        Camera feature based landmark in the Graph.
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
        self.vertices.add(vertex)
        self._table[t].add(vertex)

    @overload
    def add(self, vertices: Iterable[GraphVertex]) -> None:
        """
        @overload.
        Adds new vertices to collections based on its type.
        Args:
            vertices (tuple[GraphVertex, ...]): new vertices to be added to the graph.
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
                    vertices (tuple[GraphVertex, ...]): new vertices to be added to the graph.
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
        self.vertices.remove(vertex)
        self._table[t].remove(vertex)

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
