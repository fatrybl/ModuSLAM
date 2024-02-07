from collections import deque

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import StereoCameraOdometry
from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex


class StereoCameraOdometryFactory(EdgeFactory):
    """
    Creates edges of type: StereoCameraOdometry.
    """

    @classmethod
    def create(
        cls, graph: Graph, vertices: set[Vertex], measurements: deque[Measurement]
    ) -> list[StereoCameraOdometry]:
        edges: list[StereoCameraOdometry] = []
        return edges
