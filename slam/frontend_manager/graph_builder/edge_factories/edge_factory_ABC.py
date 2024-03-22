from abc import ABC, abstractmethod
from typing import Generic

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import GraphEdge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import GraphVertex, GtsamVertex, Vertex
from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.ordered_set import OrderedSet


class EdgeFactory(ABC, Generic[GraphEdge, GraphVertex]):
    """Abstract factory for creating edges."""

    @abstractmethod
    def __init__(self, config: EdgeFactoryConfig) -> None: ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the factory.

        Returns:
            (str): name of the factory.
        """

    @property
    @abstractmethod
    def vertex_type(self) -> type[Vertex]:
        """Type of the vertex used by the factory for edge creation.

        Returns:
            (type[Vertex]): vertex type.
        """

    @property
    @abstractmethod
    def base_vertex_type(self) -> type[GtsamVertex]:
        """Type of the base vertex used by the factory for edge creation.

        Returns:
            (type[BaseVertex]): base vertex type.
        """

    @abstractmethod
    def create(
        self, graph: Graph, vertex: GraphVertex, measurements: OrderedSet[Measurement]
    ) -> list[GraphEdge]:
        """
        Creates new edges from the given measurements.
        Args:
            graph (Graph): the main graph.
            vertex (GraphVertex): graph vertices to be used for new edges.
            measurements (OrderedSet[Measurement]): measurements from different handlers.

        Returns:
            (list[GraphEdge]): new edges.
        """
