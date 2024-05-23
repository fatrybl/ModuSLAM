from abc import ABC, abstractmethod
from typing import Any, TypeVar, Union

import gtsam

from slam.utils.numpy_types import Vector3

GtsamInstance = Union[gtsam.Pose3, gtsam.Rot3, Vector3, gtsam.NavState, gtsam.imuBias.ConstantBias]


class Vertex(ABC):
    """Base absract vertex of the Graph."""

    def __init__(self, index: int = 0, timestamp: int = 0, value: Any = None):
        self._index = index
        self._timestamp = timestamp
        self._edges: set = set()
        self._value = value

    @property
    def timestamp(self) -> int:
        """Timestamp of the vertex."""
        return self._timestamp

    @property
    def index(self) -> int:
        """Index of the vertex."""
        return self._index

    @property
    def edges(self) -> set:
        """Edges of the vertex."""
        return self._edges

    @property
    def value(self) -> Any:
        """Value of the vertex."""
        return self._value

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
    Base abstract non-optimizable vertex: does not have GTSAM properties
    and is not included in GTSAM factor graph as a variable.
    """

    @abstractmethod
    def update(self, value: Any) -> None:
        """Updates the vertex with the new value.

        Args:
            value (Any): new value.
        """


class OptimizableVertex(Vertex):
    """Base abstract optimizable vertex of the Graph with GTSAM properties and is
    included in GTSAM factor graph as a variable."""

    @property
    @abstractmethod
    def gtsam_instance(self) -> GtsamInstance:
        """GTSAM instance of the vertex."""

    @property
    @abstractmethod
    def gtsam_index(self) -> int:
        """Unique index of GTSAM instance."""
