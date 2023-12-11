import logging
from dataclasses import dataclass
from typing import Any

import gtsam
import numpy as np
import numpy.typing as npt

from slam.frontend_manager.graph.edges import Edge

logger = logging.getLogger(__name__)


@dataclass
class Vertex:
    """
    Base vertex in Graph.
    """
    id: int
    timestamp: int
    symbol: gtsam.Symbol
    edges: set[Edge]
    instance: Any


@dataclass
class State:
    """
    The state in a particular timestamp.
    Stores a set of vertices with the same timestamp.
    """
    timestamp: int
    vertices: set[Vertex]


@dataclass
class Pose(Vertex):
    """
    Pose vertex in Graph.
    """
    position: npt.NDArray[np.float64]
    rotation: npt.NDArray[np.float64]
    SE3: npt.NDArray[np.float64]


@dataclass
class Velocity(Vertex):
    """
    Linear velocity vertex in Graph.
    """


@dataclass
class Landmark(Vertex):
    """
    Landmark vertex in Graph.
    """


@dataclass
class Bias(Vertex):
    """
    Imu bias vertex in Graph.
    """
