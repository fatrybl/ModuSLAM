from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, TypeAlias, TypeVar

import gtsam
from gtsam.symbol_shorthand import B, C, F, L, M, N, V, X

if TYPE_CHECKING:
    from slam.frontend_manager.graph.edges import Edge

GtsamVertex: TypeAlias = gtsam.Rot3 | gtsam.Pose3 | gtsam.NavState


class Vertex(ABC):
    """Base absract vertex of the Graph."""

    def __init__(self):
        self.index: int = 0
        self.timestamp: int = 0
        self.edges: set[Edge] = set()
        self.base_vertex: GtsamVertex = gtsam.Pose3()

    @abstractmethod
    def update(self, values: GtsamVertex) -> None:
        """Updates the vertex with the new values.

        Args:
            values (GtsamVertex): new values.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def _gtsam_symbol(self) -> Callable[[int], int]:
        """Interface to the gtsam.symbol_shorthand.symbol.

        Returns:
            (Callable[[int], int]): gtsam.symbol_shorthand.symbol interface.
        """
        raise NotImplementedError

    @property
    def gtsam_index(self) -> int:
        """Index of the vertex of the corresponding gtsam.value.

        Returns:
            (int): index of the vertex.
        """
        return self._gtsam_symbol(self.index)


GraphVertex = TypeVar("GraphVertex", bound=Vertex)


class Pose(Vertex):
    """Pose vertex in Graph.

    TODO: check types of the attributes.
    """

    def __init__(self):
        super().__init__()
        self.position: tuple[float, ...] = self.base_vertex.translation()
        self.rotation: tuple[float, ...] = self.base_vertex.rotation()
        self.SE3: tuple[float, ...] = self.base_vertex.matrix()

    @property
    def _gtsam_symbol(self) -> Callable[[int], int]:
        return X

    def update(self, values: gtsam.Pose3) -> None:
        self.base_vertex = values
        self.position = values.translation()
        self.rotation = values.rotation()
        self.SE3 = values.matrix()


class CameraPose(Pose):
    """The pose where an image has been taken."""

    def __init__(self):
        super().__init__()

    @property
    def _gtsam_symbol(self) -> Callable[[int], int]:
        return C


class LidarPose(Pose):
    """The pose where a point-cloud has been registered."""

    def __init__(self):
        super().__init__()

    @property
    def _gtsam_symbol(self) -> Callable[[int], int]:
        return L


class Velocity(Vertex):
    """Linear velocity vertex in Graph."""

    def __init__(self):
        super().__init__()
        self.base_vertex: gtsam.VectorValues = gtsam.VectorValues()
        self.linear_velocity: tuple[float, ...] = (0, 0, 0)

    def update(self, values: gtsam.VectorValues) -> None:
        self.base_vertex = values

    @property
    def _gtsam_symbol(self) -> Callable[[int], int]:
        return V


class NavState(Vertex):
    """
    Navigation state vertex in the Graph:
        pose and velocity.
    """

    def __init__(self):
        super().__init__()
        self.base_vertex: gtsam.NavState = gtsam.NavState()
        self.velocity = self.base_vertex.velocity()
        self.pose = self.base_vertex.pose()

    def update(self, values: gtsam.NavState) -> None:
        self.base_vertex = values
        self.velocity = values.velocity()
        self.pose = values.pose()

    @property
    def _gtsam_symbol(self) -> Callable[[int], int]:
        return N


class Landmark(Vertex):
    """Base landmark in the Graph."""

    def __init__(self):
        super().__init__()
        self.base_vertex: gtsam.Point3 = gtsam.Point3()
        self.position: tuple[float, ...] = self.base_vertex

    def update(self, values: gtsam.Point3) -> None:
        self.base_vertex = values

    @property
    def _gtsam_symbol(self) -> Callable[[int], int]:
        raise M


class CameraFeature(Landmark):
    """Camera feature based landmark in the Graph."""

    def __init__(self):
        super().__init__()

    @property
    def _gtsam_symbol(self) -> Callable[[int], int]:
        return F


class ImuBias(Vertex):
    """Imu bias in the Graph."""

    def __init__(self):
        super().__init__()
        self.base_vertex: gtsam.imuBias = gtsam.imuBias.ConstantBias()
        self.accelerometer_bias = self.base_vertex.accelerometer()
        self.gyroscope_bias = self.base_vertex.gyroscope()

    def update(self, values: gtsam.imuBias.ConstantBias) -> None:
        self.base_vertex = values
        self.accelerometer_bias = values.accelerometer()
        self.gyroscope_bias = values.gyroscope()

    @property
    def _gtsam_symbol(self) -> Callable[[int], int]:
        return B
