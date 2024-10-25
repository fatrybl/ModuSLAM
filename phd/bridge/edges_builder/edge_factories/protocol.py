from typing import Protocol

from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from phd.bridge.objects.search_database import Database


class EdgeFactory(Protocol):
    @classmethod
    def create(cls, measurement, database: Database) -> tuple[list[Edge], list[Vertex]]:
        """Creates edges for the given measurement."""
