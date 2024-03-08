from collections import deque

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import LidarOdometry
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex
from slam.frontend_manager.graph_builder.edges_factories.edge_factory_ABC import (
    EdgeFactory,
)


class LidarOdometryEdgeFactory(EdgeFactory):
    """
    Creates edges of type: LidarOdometry.

    TODO: Add the implementation for single lidar odometry measurement.
    """

    @classmethod
    def create(
        cls, graph: Graph, vertex: Vertex, measurements: deque[Measurement]
    ) -> list[LidarOdometry]:
        edges: list[LidarOdometry] = []
        return edges
