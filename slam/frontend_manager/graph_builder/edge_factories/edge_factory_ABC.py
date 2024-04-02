from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Generic

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_edges import GraphEdge
from slam.frontend_manager.graph.base_vertices import GraphVertex
from slam.frontend_manager.graph.graph import Graph
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
    def vertices_types(self) -> set[type[GraphVertex]]:
        """Type of the vertices used by the factory for edge creation.

        Returns:
            (set[type[GraphVertex]]): type(s) of vertex(s).
        """

    @property
    @abstractmethod
    def base_vertices_types(self) -> set[type[GraphVertex]]:
        """Type of the base vertex used by the factory for edge creation.

        Returns:
            (type[GraphVertex]): type(s) of base vertex(s).
        """

    @abstractmethod
    def create(
        self,
        graph: Graph,
        vertices: Iterable[GraphVertex],
        measurements: OrderedSet[Measurement],
    ) -> list[GraphEdge]:
        """
        Creates new edges from the given measurements.
        Args:
            graph (Graph): the main graph.
            vertices (Iterable[GraphVertex]): graph vertices to be used for new edges.
            measurements (OrderedSet[Measurement]): measurements from different handlers.

        Returns:
            (list[GraphEdge]): new edges.
        """
