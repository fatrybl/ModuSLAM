from typing import Iterable

import gtsam

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.custom_edges import ImuOdometry
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import GraphVertex, Pose
from slam.frontend_manager.graph_builder.edge_factories.edge_factory_ABC import (
    EdgeFactory,
)
from slam.utils.ordered_set import OrderedSet


class ImuOdometryFactory(EdgeFactory):
    """
    Creates edges of type: ImuOdometry.
    """

    def __init__(self) -> None:
        self.noise_model: gtsam.noiseModel.Diagonal
        self.gtsam_factor: gtsam.ImuFactor

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def vertices_types(self) -> set[type[Pose]]:
        return {Pose}

    @property
    def base_vertices_type(self) -> set[type[gtsam.Pose3]]:
        return {gtsam.Pose3}

    def create(
        self,
        graph: Graph,
        vertices: Iterable[GraphVertex],
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
