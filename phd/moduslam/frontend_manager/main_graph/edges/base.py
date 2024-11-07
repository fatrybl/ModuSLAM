from abc import ABC, abstractmethod
from collections.abc import Collection
from typing import Generic, TypeVar

import gtsam

from phd.external.objects.measurements import Measurement
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex

V = TypeVar("V", bound=Vertex)
V1 = TypeVar("V1", bound=Vertex)
V2 = TypeVar("V2", bound=Vertex)


class Edge(ABC):
    """Base abstract edge."""

    def __init__(
        self,
        factor: gtsam.NonlinearFactor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        self._factor = factor
        self._noise_model = noise_model
        self._index: int | None = None

    @property
    def factor(self) -> gtsam.NonlinearFactor:
        """GTSAM factor."""
        return self._factor

    @property
    def noise_model(self) -> gtsam.noiseModel.Base:
        """GTSAM noise model of the factor."""
        return self._noise_model

    @property
    def index(self) -> int | None:
        """Get the unique index of the edge.

        Matches the index in the GTSAM factor graph. Raises ValueError if index is not
        set.
        """
        if self._index is None:
            raise ValueError("Index has not been set.")
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

    @abstractmethod
    @property
    def vertices(self) -> Collection[Vertex]:
        """The vertices of an edge."""


class UnaryEdge(Generic[V], Edge):
    """Unary edge for a single vertex."""

    def __init__(
        self,
        vertex: V,
        measurement: Measurement,
        factor: gtsam.NonlinearFactor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            vertex: vertex which is connected by the edge.

            measurement: measurement which formed the edge.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(factor, noise_model)
        self._vertex = vertex
        self._measurement = measurement

    @property
    def vertex(self) -> V:
        """Vertex of the edge."""
        return self._vertex

    @property
    def vertices(self) -> list[V]:
        """List with a single vertex."""
        return [self._vertex]

    @property
    def measurement(self) -> Measurement:
        """Measurement which formed the edge."""
        return self._measurement


class BinaryEdge(Generic[V1, V2], Edge):
    """Connects two vertices of the Graph."""

    def __init__(
        self,
        vertex1: V1,
        vertex2: V2,
        measurement: Measurement,
        factor: gtsam.NonlinearFactor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            vertex1: first vertex.

            vertex2: second vertex.

            measurement: measurement which formed the edge.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(factor, noise_model)
        self._vertex1 = vertex1
        self._vertex2 = vertex2
        self._measurement = measurement

    @property
    def vertex1(self) -> V1:
        """First vertex of the edge."""
        return self._vertex1

    @property
    def vertex2(self) -> V2:
        """Second vertex of the edge."""
        return self._vertex2

    @property
    def vertices(self) -> tuple[V1, V2]:
        """Vertices of the edge."""
        return self._vertex1, self._vertex2

    @property
    def measurement(self) -> Measurement:
        """Measurement which formed the edge."""
        return self._measurement


class RadialEdge(Generic[V1, V2], Edge):
    """Connects a vertex with multiple vertices."""

    def __init__(
        self,
        center: V1,
        radials: list[V2],
        measurements: list[Measurement],
        factor: gtsam.NonlinearFactor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            measurements: measurements which formed the edge.

            center: base central vertex.

            radials: other vertices.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(factor, noise_model)
        self._center = center
        self._radials = radials
        self._measurements = measurements

    @property
    def central_vertex(self) -> V1:
        """Central vertex of the edge."""
        return self._center

    @property
    def radial_vertices(self) -> list[V2]:
        """Radial vertices of the edge."""
        return self._radials

    @property
    def vertices(self) -> list[V1 | V2]:
        """Vertices of the edge."""
        return [self._center, *self._radials]

    @property
    def measurements(self) -> list[Measurement]:
        """Measurements which formed the edge."""
        return self._measurements


class MultiEdge(Generic[V], Edge):
    """Connecting multiple vertices."""

    def __init__(
        self,
        vertices: list[V],
        measurements: list[Measurement],
        factor: gtsam.NonlinearFactor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            vertices: vertices which are connected by the edge.

            measurements: measurements which formed the edge.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(factor, noise_model)
        self._vertices = vertices
        self._measurements = measurements

    @property
    def vertices(self) -> list[V]:
        """Vertices of the edge."""
        return self._vertices

    @property
    def measurements(self) -> list[Measurement]:
        """Measurements which formed the edge."""
        return self._measurements
