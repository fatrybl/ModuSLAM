from abc import ABC, abstractmethod
from typing import Any, TypeVar, Union

import gtsam

from src.moduslam.custom_types.aliases import Vector3

GtsamInstance = Union[gtsam.Pose3, gtsam.Rot3, Vector3, gtsam.NavState, gtsam.imuBias.ConstantBias]


class Vertex(ABC):
    """Base absract vertex of the Graph."""

    def __init__(self, index: int, value: Any = None):
        if index < 0:
            raise ValueError("Index must be non-negative.")
        self._index = index
        self._value = value

    @property
    def index(self) -> int:
        """Index of the vertex."""
        return self._index

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


V = TypeVar("V", bound=Vertex)
"""TypeVar for the Graph vertices."""
