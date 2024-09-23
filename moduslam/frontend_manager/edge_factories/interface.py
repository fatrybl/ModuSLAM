from typing import Protocol, runtime_checkable

from moduslam.frontend_manager.graph.base_edges import BaseEdge
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.utils.ordered_set import OrderedSet


@runtime_checkable
class EdgeFactory(Protocol[BaseEdge]):
    """Abstract factory for creating edges."""

    def __init__(self, *args, **kwargs):
        """Initializes the handler.

        Args:
            config: configuration of the handler.
        """

    @property
    def name(self) -> str:
        """Unique factory name."""

    def create(
        self,
        graph: Graph,
        measurements: OrderedSet[Measurement],
        timestamp: int,
    ) -> list[BaseEdge]:
        """Creates new edges from the measurements.

        Args:
            graph: the graph to create edges for.

            measurements: measurements from different handlers.

            timestamp: the final timestamp for the edge(s).

        Returns:
            new edge(s).
        """
