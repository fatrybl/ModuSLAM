from collections import deque

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import SmartStereoLandmark
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex
from slam.frontend_manager.graph_builder.edges_factories.edge_factory_ABC import (
    EdgeFactory,
)


class SmartStereoFeaturesFactory(EdgeFactory):
    """
    Creates edges of type: SmartStereoLandmarkFactor.
    """

    @classmethod
    def create(
        cls, graph: Graph, vertex: Vertex, measurements: deque[Measurement]
    ) -> list[SmartStereoLandmark]:
        edges: list[SmartStereoLandmark] = []
        return edges
