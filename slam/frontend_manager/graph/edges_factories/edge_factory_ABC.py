from abc import ABC, abstractmethod
from collections import deque
from typing import Generic, TypeVar

from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import Edge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex

E = TypeVar("E", bound=Edge)


class EdgeFactory(ABC, Generic[E]):
    """
    Abstract factory for creating edges_123.
    """

    @classmethod
    @abstractmethod
    def create(cls, graph: Graph, vertices: set[Vertex], measurements: deque[Measurement]) -> list[E]:
        """
        Creates new edges_123 from the given measurements.
        Args:
            graph (Graph): the main graph.
            vertices (set[Vertex]): graph vertices to be used for new edges.
            measurements (deque[Measurement]): measurements from different handlers.

        Returns:
            (list[E]): new edges.
        """
