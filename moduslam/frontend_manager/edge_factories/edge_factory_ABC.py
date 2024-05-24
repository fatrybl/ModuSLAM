from abc import ABC, abstractmethod
from typing import Generic

from moduslam.frontend_manager.graph.base_edges import GraphEdge
from moduslam.frontend_manager.graph.base_vertices import GraphVertex, GtsamInstance
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.utils.ordered_set import OrderedSet


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
        measurements: OrderedSet[Measurement],
        timestamp: int,
    ) -> list[GraphEdge]:
        """Creates new edges from the measurements.

        Args:
            graph: the graph to create edges for.

            measurements: measurements from different handlers.

            timestamp: final timestamp.

        Returns:
            new edges.
        """
