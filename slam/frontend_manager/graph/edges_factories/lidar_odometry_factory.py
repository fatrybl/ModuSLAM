from collections import deque

from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import LidarOdometry
from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex


class LidarOdometryFactory(EdgeFactory):
    """
    Creates edges of type: LidarOdometry.
    """

    @classmethod
    def create(cls, graph: Graph, vertices: set[Vertex], measurements: deque[Measurement]) -> list[LidarOdometry]:
        edges: list[LidarOdometry] = []
        return edges
