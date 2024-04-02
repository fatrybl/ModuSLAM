from abc import ABC, abstractmethod
from typing import Any, TypeVar


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
    def gtsam_index(self) -> int:
        """Unique index of the variable in the GTSAM Values.

        Returns:
            (int): index.
        """


GraphVertex = TypeVar("GraphVertex", bound=Vertex)
