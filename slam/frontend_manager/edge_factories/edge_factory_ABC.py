from abc import ABC, abstractmethod
from collections.abc import Collection
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
            name of the factory (str).
        """
        return self._name

    @property
    @abstractmethod
    def vertices_types(self) -> set[type[GraphVertex]]:
        """Types of the vertices used by the factory for edge creation.

        Returns:
            type(s) of vertex(s) (set[type[GraphVertex]]).
        """

    @property
    @abstractmethod
    def base_vertices_types(self) -> set[type[GraphVertex]]:
        """Types of the base vertices (aka GTSAM types) used by the factory for edge
        creation.

        Returns:
            type(s) of base vertex(s) (type[GraphVertex]).
        """

    @staticmethod
    @abstractmethod
    def noise_model(
        values: Collection[float],
    ) -> gtsam.noiseModel.Base:
        """Measurement noise model method.

        Args:
            values (Collection[float]): measurement noise covariance.

        Returns:
            noise model (gtsam.noiseModel.Base).
        """

    @abstractmethod
    def create(
        self,
        graph: Graph,
        vertices: Collection[GraphVertex],
        measurements: OrderedSet[Measurement],
    ) -> list[GraphEdge]:
        """
        Creates new edges from the given measurements.
        Args:
            graph (Graph): the main graph.
            vertices (Collection[GraphVertex]): graph vertices to be used for new edges.
            measurements (OrderedSet[Measurement]): measurements from different handlers.

        Returns:
            new edges (list[GraphEdge]).
        """
