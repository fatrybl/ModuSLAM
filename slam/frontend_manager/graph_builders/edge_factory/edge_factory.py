import logging
from collections import deque

from slam.frontend_manager.elements_distributor.measurement import Measurement
from slam.frontend_manager.graph.edges.base_edge import Edge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex
from slam.frontend_manager.handlers.ABC_handler import ElementHandler

logger = logging.getLogger(__name__)


class EdgeFactory:
    @classmethod
    def create_edge(
        cls,
        graph: Graph,
        vertex: Vertex,
        handler: ElementHandler,
        measurements: deque[Measurement],
    ) -> Edge:
        pass
