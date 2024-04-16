from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import Generic

import gtsam

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

    def __init__(self, config: EdgeFactoryConfig):
        self._name = config.name

    @property
    def name(self) -> str:
        """Name of the factory.

        Returns:
            (str): name of the factory.
        """
        return self._name

    @property
    @abstractmethod
    def vertices_types(self) -> set[type[GraphVertex]]:
        """Types of the vertices used by the factory for edge creation.

        Returns:
            (set[type[GraphVertex]]): type(s) of vertex(s).
        """

    @property
    @abstractmethod
    def base_vertices_types(self) -> set[type[GraphVertex]]:
        """Types of the base vertices (aka GTSAM types) used by the factory for edge
        creation.

        Returns:
            (type[GraphVertex]): type(s) of base vertex(s).
        """

    @staticmethod
    @abstractmethod
    def noise_model(values: Iterable[float]) -> Callable[[Iterable[float]], gtsam.noiseModel.Base]:
        """Measurement noise model method.

        Returns:
            noise model (gtsam.noiseModel.Base).
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
