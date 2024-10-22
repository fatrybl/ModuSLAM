from typing import Protocol

from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from phd.bridge.objects.graph_candidate import VertexCluster
from phd.moduslam.frontend_manager.graph.graph import Graph


class EdgeFactory(Protocol):
    @classmethod
    def create(
        cls, measurement, graph: Graph, vertices_db: list[VertexCluster]
    ) -> tuple[list[Edge], list[Vertex]]:
        """Creates edges for the given measurement."""
