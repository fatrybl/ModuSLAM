from abc import ABC, abstractmethod
from typing import Any, TypeVar, Union

import gtsam

from moduslam.types.aliases import Vector3

GtsamInstance = Union[gtsam.Pose3, gtsam.Rot3, Vector3, gtsam.NavState, gtsam.imuBias.ConstantBias]


class Vertex(ABC):
    """Base absract vertex of the Graph."""

    def __init__(self, index: int = 0, value: Any = None):
        self._index = index
        self._value = value

    @property
    def index(self) -> int:
        """Index of the vertex."""
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        """Sets the index of the vertex.

        Attention: the index is set automatically when the vertex is added to the graph.

        Args:
            value: new index.

        Raises:
            ValueError: if the index is negative.
        """
        if value < 0:
            raise ValueError("Index must be non-negative")
        self._index = value

    @property
    def value(self) -> Any:
        """Value of the vertex."""
        return self._value

    @abstractmethod
    def update(self, value: Any, *args, **kwargs) -> None:
        """Updates the vertex with the new value.

        Args:
            value: new value.

            *args: additional arguments.

            **kwargs: additional keyword arguments.
        """


class NonOptimizableVertex(Vertex):
    """Base class for not optimizable vertex of the Graph."""

    @abstractmethod
    def update(self, value: Any, *args, **kwargs) -> None: ...


class OptimizableVertex(Vertex):
    """Base abstract optimizable vertex of the Graph with GTSAM properties and is
    included in GTSAM factor graph as a variable."""

    @property
    @abstractmethod
    def backend_instance(self) -> GtsamInstance:
        """External backend instance of the vertex."""

    @property
    @abstractmethod
    def backend_index(self) -> int:
        """Unique external backend index of an instance."""


BaseVertex = TypeVar("BaseVertex", bound=Vertex)
"""TypeVar for the Graph vertices."""
