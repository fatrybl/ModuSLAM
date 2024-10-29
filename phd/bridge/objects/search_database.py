from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)


class Database:
    """Database for storing and searching vertices."""

    def __init__(self, graph: Graph):
        """
        TODO:
            1) Change graph to be able to use clusters.
        """
        self._graph = graph

    def expand(self, cluster: VertexCluster):
        """Expands the database with the new cluster."""
        raise NotImplementedError
