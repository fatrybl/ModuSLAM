from abc import ABC, abstractmethod
from typing import Any, TypeVar, Union

import gtsam

from slam.utils.numpy_types import Vector3

GtsamValue = Union[gtsam.Pose3, gtsam.Rot3, Vector3, gtsam.NavState, gtsam.imuBias.ConstantBias]


class Vertex(ABC):
    """Base absract vertex of the Graph."""

    def __init__(self):
        self.index: int = 0
        self.timestamp: int = 0
        self.edges = set()
        self.value: Any = None

    @abstractmethod
    def update(self, values: Any) -> None:
        """Updates the vertex with the new values.

        Args:
            values (Any): new values.
        """


class OptimizableVertex(Vertex):
    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def gtsam_value(self) -> GtsamValue:
        """GTSAM value of the vertex.

        Returns:
            value (GtsamValue).
        """

    @property
    @abstractmethod
    def gtsam_index(self) -> int:
        """Unique index of the variable in the GTSAM Values.

        Returns:
            index (int).
        """


GraphVertex = TypeVar("GraphVertex", bound=Vertex)
