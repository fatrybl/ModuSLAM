from abc import ABC, abstractmethod
from collections.abc import Collection, Sequence
from typing import Generic, TypeVar

import gtsam

from moduslam.frontend_manager.measurement_storage import Measurement
from phd.moduslam.frontend_manager.graph.vertices.base import BaseVertex


class Edge(ABC, Generic[BaseVertex]):
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
        self._index: int = 0

    @property
    def factor(self) -> gtsam.NonlinearFactor:
        """GTSAM factor."""
        return self._factor

    @property
    def noise_model(self) -> gtsam.noiseModel.Base:
        """GTSAM noise model of the factor."""
        return self._noise_model

    @property
    def index(self) -> int:
        """Unique index of the edge.

        Corresponds to the index of the factor in the factor graph.
        """
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        """
        Attention:
            Set index only when you really need it.

        Index is being set automatically when an edge is added to the graph.

        Args:
            value: new index.

        Raises:
            ValueError: if the index is negative.
        """
        if value < 0:
            raise ValueError("Index should be non-negative.")

        self._index = value

    @property
    @abstractmethod
    def vertices(self) -> Collection[BaseVertex]:
        """The vertices of an edge."""


class UnaryEdge(Edge, Generic[BaseVertex]):
    """Connects one vertex of the Graph (unary factor)."""

    def __init__(
        self,
        vertex: BaseVertex,
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
    def vertex(self) -> BaseVertex:
        """Vertices of the edge."""
        return self._vertex

    @property
    def measurement(self) -> Measurement:
        """Measurement which formed the edge."""
        return self._measurement

    @property
    def vertices(self) -> Collection[BaseVertex]:
        """The vertices of an edge."""
        return (self._vertex,)


class BinaryEdge(Edge, Generic[BaseVertex]):
    """Connects two vertices of the Graph."""

    def __init__(
        self,
        vertex1: BaseVertex,
        vertex2: BaseVertex,
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
    def vertex1(self) -> BaseVertex:
        """First vertex of the edge."""
        return self._vertex1

    @property
    def vertex2(self) -> BaseVertex:
        """Second vertex of the edge."""
        return self._vertex2

    @property
    def vertices(self) -> tuple[BaseVertex, BaseVertex]:
        """Vertices of the edge."""
        return self._vertex1, self._vertex2

    @property
    def measurement(self) -> Measurement:
        """Measurement which formed the edge."""
        return self._measurement


class RadialEdge(Edge, Generic[BaseVertex]):
    """Connects a vertex with multiple vertices."""

    def __init__(
        self,
        center: BaseVertex,
        radials: Sequence[BaseVertex],
        measurements: Sequence[Measurement],
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
    def central_vertex(self) -> BaseVertex:
        """Central vertex of the edge."""
        return self._center

    @property
    def radial_vertices(self) -> Sequence[BaseVertex]:
        """Radial vertices of the edge."""
        return self._radials

    @property
    def vertices(self) -> tuple[BaseVertex, ...]:
        """Vertices of the edge."""
        return self._center, *self._radials

    @property
    def measurements(self) -> Sequence[Measurement]:
        """Measurements which formed the edge."""
        return self._measurements


class MultiEdge(Edge, Generic[BaseVertex]):
    """Connecting multiple vertices."""

    def __init__(
        self,
        vertices: list[BaseVertex],
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
    def vertices(self) -> list[BaseVertex]:
        """Vertices of the edge."""
        return self._vertices

    @property
    def measurements(self) -> list[Measurement]:
        """Measurements which formed the edge."""
        return self._measurements


BaseEdge = TypeVar("BaseEdge", bound=Edge)
"""TypeVar for GraphEdge."""
