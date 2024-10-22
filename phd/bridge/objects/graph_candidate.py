from dataclasses import dataclass, field

from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from phd.moduslam.frontend_manager.graph.graph import Graph


@dataclass
class VertexCluster:
    vertices: list[Vertex] = field(default_factory=lambda: [])


class Candidate:
    """Graph candidate.

    Stores new edges and vertices to be added to the graph.
    """

    def __init__(self, graph: Graph):
        self._graph = graph
        self._edges: list[Edge] = []
        self._clusters: list[VertexCluster] = []

    @property
    def graph(self) -> Graph:
        """Graph."""
        return self._graph

    @property
    def edges(self) -> list[Edge]:
        """Edges to be added to the graph."""
        return self._edges

    @property
    def clusters(self) -> list[VertexCluster]:
        """Clusters to be added to the graph."""
        return self._clusters

    def add_edges(self, edges: list[Edge]):
        """Adds edges to the candidate."""
        self._edges += edges

    def add_cluster(self, cluster: VertexCluster):
        """Adds a cluster to the candidate."""
        self._clusters.append(cluster)
