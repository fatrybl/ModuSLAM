from abc import ABC, abstractmethod
from collections.abc import Collection

import gtsam

from phd.measurements.processed import Measurement
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex


class Edge(ABC):
    """Base abstract edge."""

    def __init__(self):
        self._index: int | None = None

    @property
    @abstractmethod
    def factor(self) -> gtsam.NonlinearFactor:
        """GTSAM factor."""

    @property
    @abstractmethod
    def vertices(self) -> Collection[Vertex]:
        """The vertex(s) of an edge."""

    @property
    @abstractmethod
    def measurement(self) -> Measurement:
        """A measurement which formed the edge."""

    @property
    def index(self) -> int | None:
        """The unique index of an edge.

        Matches the index in the GTSAM factor graph.
        Attention:
        the index is being set automatically when the corresponding edge is added to the graph.
        Do not set it manually elsewhere.
        """
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        """Attention:
        the index is being set automatically when the corresponding edge is added to the graph.
        Do not set it manually elsewhere.

        Args:
            value: new index.

        Raises:
            ValueError: if the index is negative.
        """
        if value < 0:
            raise ValueError("Index should be non-negative.")

        self._index = value


class UnaryEdge(Edge):
    """Unary abstract edge for a single vertex."""

    @property
    @abstractmethod
    def vertex(self) -> Vertex:
        """Vertex of the edge."""


class BinaryEdge(Edge):
    """Abstract edge to connect two vertices."""

    @property
    @abstractmethod
    def vertex1(self) -> Vertex:
        """First vertex of the edge."""

    @property
    @abstractmethod
    def vertex2(self) -> Vertex:
        """Second vertex of the edge."""

    @property
    def vertices(self) -> tuple[Vertex, Vertex]:
        return self.vertex1, self.vertex2


class RadialEdge(Edge):
    """Connects a vertex with multiple vertices."""

    @property
    @abstractmethod
    def central_vertex(self) -> Vertex:
        """Central vertex of the edge."""

    @property
    @abstractmethod
    def radial_vertices(self) -> Collection[Vertex]:
        """Radial vertices of the edge."""
