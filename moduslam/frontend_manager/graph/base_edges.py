from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import gtsam

from moduslam.frontend_manager.graph.base_vertices import GraphVertex
from moduslam.frontend_manager.measurement_storage import Measurement


class Edge(ABC, Generic[GraphVertex]):
    """Base abstract edge."""

    def __init__(
        self,
        measurements: tuple[Measurement, ...],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            measurements: measurements which formed the edge.
            factor: GTSAM factor.
            noise_model: GTSAM noise model of the factor.
        """
        self.measurements = measurements
        self.factor = factor
        self.noise_model = noise_model
        self._index: int = 0

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

        Index is being set automatically when the edge is added to the graph.

        Args:
            value (int): new index.

        Raises:
            ValueError: if the index is negative.
        """
        if value < 0:
            raise ValueError("Index should be non-negative.")

        self._index = value

    @property
    @abstractmethod
    def all_vertices(self) -> set[GraphVertex]:
        """Vertices of the edge."""


class MultiEdge(Edge):
    """Base class for all multi-edges in the Graph. Multi-edge connects two sets of
    vertices.

    Args:
        vertex_set_1: first set of vertices.

        vertex_set_2: second set of vertices.

        measurements: measurements which formed the edge.

        factor: GTSAM factor.

        noise_model: GTSAM noise model of the factor.
    """

    def __init__(
        self,
        vertex_set_1: set[GraphVertex],
        vertex_set_2: set[GraphVertex],
        measurements: tuple[Measurement, ...],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            vertex_set_1: first set of vertices.

            vertex_set_2: second set of vertices.

            measurements: measurements which formed the edge.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(measurements, factor, noise_model)
        self.vertex_set_1 = vertex_set_1
        self.vertex_set_2 = vertex_set_2

    @property
    def all_vertices(self) -> set[GraphVertex]:
        """Vertices of the edge."""
        return self.vertex_set_1.union(self.vertex_set_2)


class UnaryEdge(Edge):
    """Edge to connect one vertex of the Graph (aka unary factor)."""

    def __init__(
        self,
        vertex: GraphVertex,
        measurements: tuple[Measurement, ...],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            vertex: vertex which is connected by the edge.

            measurements: measurements which formed the edge.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(measurements, factor, noise_model)
        self.vertex = vertex

    @property
    def all_vertices(self) -> set[GraphVertex]:
        """Vertices of the edge."""
        return {self.vertex}


class BinaryEdge(Edge):
    """Edge to connect two vertices of the Graph."""

    def __init__(
        self,
        vertex1: GraphVertex,
        vertex2: GraphVertex,
        measurements: tuple[Measurement, ...],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            vertex1: first vertex.
            vertex2: second vertex.
            measurements: measurements which formed the edge.
            factor: GTSAM factor.
            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(measurements, factor, noise_model)
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    @property
    def all_vertices(self) -> set[GraphVertex]:
        """Vertices of the edge."""
        return {self.vertex1, self.vertex2}


class CalibrationEdge(Edge):
    """Edge connects calibration vertex with other vertices."""

    def __init__(
        self,
        measurements: tuple[Measurement, ...],
        vertex: GraphVertex,
        vertices: set[GraphVertex],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            measurements: measurements which formed the edge.
            vertex: calibration vertex.
            vertices: other vertices.
            factor: GTSAM factor.
            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(measurements, factor, noise_model)
        self.vertex = vertex
        self.vertices = vertices

    @property
    def all_vertices(self) -> set[GraphVertex]:
        """Vertices of the edge."""
        return {self.vertex}.union(self.vertices)


GraphEdge = TypeVar("GraphEdge", bound=Edge)
"""TypeVar for GraphEdge."""
