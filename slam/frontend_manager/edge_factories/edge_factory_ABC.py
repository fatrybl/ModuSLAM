from abc import ABC, abstractmethod
from collections.abc import Collection
from typing import Generic

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_edges import GraphEdge
from slam.frontend_manager.graph.base_vertices import GraphVertex, GtsamInstance
from slam.frontend_manager.graph.graph import Graph
from slam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.ordered_set import OrderedSet


class EdgeFactory(ABC, Generic[GraphEdge, GraphVertex]):
    """Abstract factory for creating edges."""

    def __init__(self, config: EdgeFactoryConfig):
        """
        Args:
            config: configuration of the factory.
        """
        self._name = config.name

    @property
    def name(self) -> str:
        """Unique name of the factory."""
        return self._name

    @property
    @abstractmethod
    def vertices_types(self) -> set[type[GraphVertex]]:
        """Types of the used vertices.

        Returns:
            set of vertices types.
        """

    @property
    @abstractmethod
    def base_vertices_types(self) -> set[type[GtsamInstance]]:
        """Types of the used base (GTSAM) instances.

        Returns:
            set of base vertices types.
        """

    @abstractmethod
    def create(
        self,
        graph: Graph,
        vertices: Collection[GraphVertex],
        measurements: OrderedSet[Measurement],
    ) -> list[GraphEdge]:
        """Creates new edges from the measurements.

        Args:
            graph: the graph to create edges for.

            vertices: graph vertices to be used for new edges.

            measurements: measurements from different handlers.

        Returns:
            new edges.
        """
