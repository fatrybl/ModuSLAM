from collections import deque

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import SmartStereoLandmark
from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex


class SmartStereoFeaturesFactory(EdgeFactory):
    """
    Creates edges of type: SmartStereoLandmarkFactor.
    """

    @classmethod
    def create(cls, graph: Graph, vertices: set[Vertex], measurements: deque[Measurement]) -> list[SmartStereoLandmark]:
        edges: list[SmartStereoLandmark] = []
        return edges
