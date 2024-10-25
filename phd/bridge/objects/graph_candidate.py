from moduslam.frontend_manager.graph.base_edges import Edge
from phd.bridge.objects.vertices_cluster import Cluster


class Candidate:
    """Graph candidate.

    Stores new edges and vertices to be added to the graph.
    """

    def __init__(self):
        self._edges: list[Edge] = []
        self._clusters: list[Cluster] = []

    @property
    def edges(self) -> list[Edge]:
        """Edges to be added to the graph."""
        return self._edges

    @property
    def clusters(self) -> list[Cluster]:
        """Clusters to be added to the graph."""
        return self._clusters

    def add_edges(self, edges: list[Edge]):
        """Adds edges to the candidate."""
        self._edges += edges

    def add_cluster(self, cluster: Cluster):
        """Adds a cluster to the candidate."""
        self._clusters.append(cluster)
