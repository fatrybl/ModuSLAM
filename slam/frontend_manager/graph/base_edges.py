from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import gtsam

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_vertices import GraphVertex


class Edge(ABC, Generic[GraphVertex]):
    """Base class for all edges in the Graph."""

    def __init__(
        self,
        measurements: tuple[Measurement, ...],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        self.measurements = measurements
        self.factor = factor
        self.noise_model = noise_model
        self._index: int = 0

    @property
    def index(self) -> int:
        """Unique index of the edge. Corresponds to the index of the factor in the
        factor graph.

        Returns:
            index (int).
        """
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        """
        ATTENTION: Set index only when you really need it.
        Index is being set automatically when the edge is added to the graph.

        Args:
            value (int): new index.
        """
        if value < 0:
            raise ValueError("Index should be non-negative.")

        self._index = value

    @property
    @abstractmethod
    def all_vertices(self) -> set[GraphVertex]:
        """All vertices used by the edge.

        Returns:
            vertices (set[GraphVertex]).
        """


class MultiEdge(Edge):
    """Base class for all multi-edges in the Graph. Multi-edge connects two sets of
    vertices.

    Args:
        vertex_set_1 (set[GraphVertex]): first set of vertices.
        vertex_set_2 (set[GraphVertex]): second set of vertices.
        measurements (tuple[Element, ...]): elements of DataBatch which create the edge.
        factor (gtsam.Factor): factor from GTSAM library.
        noise_model (gtsam.noiseModel.Base): noise model for the factor.
    """

    def __init__(
        self,
        vertex_set_1: set[GraphVertex],
        vertex_set_2: set[GraphVertex],
        measurements: tuple[Measurement, ...],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        super().__init__(measurements, factor, noise_model)
        self.vertex_set_1 = vertex_set_1
        self.vertex_set_2 = vertex_set_2

    @property
    def all_vertices(self) -> set[GraphVertex]:
        return self.vertex_set_1.union(self.vertex_set_2)


class UnaryEdge(Edge):
    """Edge to connect one vertex of the Graph (aka Unary Factor).

    Args:
        measurements (tuple[Measurement, ...]): element of DataBatch which create the edge.
        vertex (GraphVertex): vertex which is connected by the edge.
        factor (gtsam.Factor): factor from GTSAM library.
        noise_model (gtsam.noiseModel.Base): noise model for the factor.
    """

    def __init__(
        self,
        vertex: GraphVertex,
        measurements: tuple[Measurement, ...],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        super().__init__(measurements, factor, noise_model)
        self.vertex = vertex

    @property
    def all_vertices(self) -> set[GraphVertex]:
        return {self.vertex}


class BinaryEdge(Edge):
    """Edge to connect two vertices of the Graph.

    Args:
        measurements (tuple[Measurement, ...]): elements of DataBatch which create the edge.
        vertex1 (GraphVertex): first vertex which is connected by the edge.
        vertex2 (GraphVertex): second vertex which is connected by the edge.
        factor (gtsam.Factor): factor from GTSAM library.
        noise_model (gtsam.noiseModel.Base): noise model for the factor.
    """

    def __init__(
        self,
        vertex1: GraphVertex,
        vertex2: GraphVertex,
        measurements: tuple[Measurement, ...],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        super().__init__(measurements, factor, noise_model)
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    @property
    def all_vertices(self) -> set[GraphVertex]:
        return {self.vertex1, self.vertex2}


class CalibrationEdge(Edge):
    """Edge for calibration factor."""

    def __init__(
        self,
        measurements: tuple[Measurement, ...],
        vertex: GraphVertex,
        vertices: set[GraphVertex],
        factor: gtsam.Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        super().__init__(measurements, factor, noise_model)
        self.vertex = vertex
        self.vertices = vertices

    @property
    def all_vertices(self) -> set[GraphVertex]:
        return {self.vertex}.union(self.vertices)


GraphEdge = TypeVar("GraphEdge", bound=Edge)
