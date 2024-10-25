from phd.bridge.objects.vertices_cluster import Cluster
from phd.moduslam.frontend_manager.graph.graph import Graph


class Database:
    """Database for storing and searching vertices."""

    def __init__(self, graph: Graph):
        """
        TODO:
            1) Change graph to be able to use clusters.
        """
        self._graph = graph

    def expand(self, cluster: Cluster):
        """Expands the database with the new cluster."""
        raise NotImplementedError
