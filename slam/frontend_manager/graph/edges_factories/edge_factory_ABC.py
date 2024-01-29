from abc import ABC, abstractmethod

from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges.base_edge import Edge
from slam.frontend_manager.graph.graph import Graph


class EdgeFactory(ABC):
    """
    Abstract factory for creating edges.
    """

    @classmethod
    @abstractmethod
    def create(cls, graph: Graph, measurements: tuple[Measurement, ...]) -> tuple[Edge, ...]:
        """
        Creates new edges from the given measurements.
        Args:
            graph (Graph): The main graph.
            measurements (tuple[Measurement]): measurements from different handlers.

        Returns:
            (tuple[Type[Edge], ...]): edges of the same type.
        """
