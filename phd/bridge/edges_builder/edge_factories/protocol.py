from typing import Protocol

from phd.moduslam.frontend_manager.main_graph.element import GraphElement
from phd.moduslam.frontend_manager.main_graph.graph import Graph


class EdgeFactory(Protocol):
    @classmethod
    def create(cls, measurement, graph: Graph) -> list[GraphElement]:
        """Creates edges for the given measurement."""
