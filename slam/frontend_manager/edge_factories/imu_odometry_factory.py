from collections.abc import Collection
from typing import Iterable

import gtsam

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_vertices import GraphVertex
from slam.frontend_manager.graph.custom_edges import ImuOdometry
from slam.frontend_manager.graph.custom_vertices import Pose
from slam.frontend_manager.graph.graph import Graph
from slam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.ordered_set import OrderedSet


class ImuOdometryFactory(EdgeFactory):
    """
    Creates edges of type: ImuOdometry.
    """

    def __init__(self, config: EdgeFactoryConfig) -> None:
        super().__init__(config)
        self._time_margin: int = config.search_time_margin

    @property
    def vertices_types(self) -> set[type[Pose]]:
        return {Pose}

    @property
    def base_vertices_type(self) -> set[type[gtsam.Pose3]]:
        return {gtsam.Pose3}

    def create(
        self,
        graph: Graph,
        vertices: Collection[GraphVertex],
        measurements: OrderedSet[Measurement],
    ) -> list[ImuOdometry]:
        """
        Creates new edges from the given measurements.
        Args:
            graph (Graph): the main graph.
            vertices (Iterable[GraphVertex]): graph vertices to be used for new edges.
            measurements (OrderedSet[Measurement]): measurements from different handlers.

        Returns:
            (list[GraphEdge]): new edges.
        """
        raise NotImplementedError
