from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar

import gtsam

if TYPE_CHECKING:
    from slam.frontend_manager.graph.edges import Edge


@dataclass(init=False, kw_only=True)
class Vertex:
    """Base vertex in Graph."""

    id: int
    timestamp: int
    symbol: str
    instance: gtsam
    edges: set[Edge] = field(default_factory=set)


GraphVertex = TypeVar("GraphVertex", bound=Vertex)


@dataclass(init=False)
class Pose(Vertex):
    """Pose vertex in Graph."""

    position: tuple[float, ...]
    rotation: tuple[float, ...]
    SE3: tuple[float, ...]
    symbol = "X"
    instance = gtsam.Pose3()


@dataclass(init=False)
class CameraPose(Pose):
    """The pose where an image has been taken."""


@dataclass(init=False)
class LidarPose(Pose):
    """The pose where a point-cloud has been registered."""


@dataclass(init=False)
class Velocity(Vertex):
    """Linear velocity vertex in Graph."""

    symbol = "V"


@dataclass(init=False)
class NavState(Vertex):
    """
    Navigation state vertex in the Graph:
        pose and velocity.
    """

    symbol = "NavState"
    instance = gtsam.NavState()
    velocity: tuple[float, ...]


@dataclass(init=False)
class Landmark(Vertex):
    """Base landmark in the Graph."""

    symbol = "L"


@dataclass(init=False)
class CameraFeature(Landmark):
    """Camera feature based landmark in the Graph."""


@dataclass(init=False)
class ImuBias(Vertex):
    """Imu bias in the Graph."""

    symbol = "ImuBias"
