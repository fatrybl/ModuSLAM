from abc import ABC, abstractmethod
from typing import Any, TypeVar, Union

import gtsam

from slam.utils.numpy_types import Vector3

GtsamInstance = Union[gtsam.Pose3, gtsam.Rot3, Vector3, gtsam.NavState, gtsam.imuBias.ConstantBias]


class Vertex(ABC):
    """Base absract vertex of the Graph."""

    def __init__(self):
        self.index: int = 0
        self.timestamp: int = 0
        self.edges = set()
        self.value: Any = None

    @abstractmethod
    def update(self, value: Any) -> None:
        """Updates the vertex with the new value.

        Args:
            value (Any): new value.
        """


GraphVertex = TypeVar("GraphVertex", bound=Vertex)
"""TypeVar for the Graph vertices."""


class NotOptimizableVertex(Vertex):
    """
    Base abstract non-optimizable vertex: does not have a GTSAM index & value,
    and is not included in GTSAM factor graph directly.
    """

    @abstractmethod
    def update(self, value: Any) -> None:
        """Updates the vertex with the new value.

        Args:
            value (Any): new value.
        """


class OptimizableVertex(Vertex):
    """Base abstract optimizable vertex of the Graph: has a GTSAM index & value,
    and is included in GTSAM factor graph."""

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def gtsam_instance(self) -> GtsamInstance:
        """GTSAM instance of the vertex."""

    @property
    @abstractmethod
    def gtsam_index(self) -> int:
        """Unique index of GTSAM instance."""
