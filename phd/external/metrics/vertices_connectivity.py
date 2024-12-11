"""Checks if a Graph Candidate is fully connected with the main graph."""

from phd.external.metrics.base import Metrics
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex


class UnionFind:
    """The Union-Find algorithm or (Disjoint-Set Union (DSU)) or simply Disjoint-Set
    Data Structure.

    It is a fundamental data structure used to solve the Dynamic Connectivity Problem,
    where the goal is to efficiently determine and merge connected components in a
    graph.
    """

    def __init__(self) -> None:
        """
        parent: A dictionary mapping each element to its parent in the disjoint set.
        rank: A dictionary mapping each element to its rank (used for balancing the tree).
        """
        self._parent: dict[Vertex, Vertex] = {}
        self._rank: dict[Vertex, int] = {}

    def find(self, vertex: Vertex) -> Vertex:
        """Finds the representative (root) of the set containing the given vertex. Uses
        path compression to flatten the tree, making future queries faster.

        Notes:
            If vertex is not already in the structure, it will be initialized as its own parent.

        Args:
            vertex: a vertex to find the representative for.

        Returns:
            a representative vertex of the set containing itself.
        """
        if vertex not in self._parent:
            self._parent[vertex] = vertex
            self._rank[vertex] = 0
        if self._parent[vertex] != vertex:
            self._parent[vertex] = self.find(self._parent[vertex])
        return self._parent[vertex]

    def union(self, v1: Vertex, v2: Vertex) -> None:
        """Merges the sets containing the vertices v1 and v2. Uses rank to keep the tree
        balanced, attaching the smaller tree under the larger one.

        Notes:
            If v1 and v2 are already in the same set, this operation does nothing.
            Otherwise, the smaller tree (by rank) will become a subtree of the larger tree.

        Args:
            v1: the first vertex to union.
            v2: the second vertex to union.
        """
        root_v1 = self.find(v1)
        root_v2 = self.find(v2)
        if root_v1 != root_v2:
            if self._rank[root_v1] > self._rank[root_v2]:
                self._parent[root_v2] = root_v1
            elif self._rank[root_v1] < self._rank[root_v2]:
                self._parent[root_v1] = root_v2
            else:
                self._parent[root_v2] = root_v1
                self._rank[root_v1] += 1


def check_connectivity(
    edges: list[Edge], old_vertices: set[Vertex], new_vertices: set[Vertex]
) -> bool:
    """Checks the connectivity of new vertices with old vertices by the edges.

    Args:
        edges: edges to check the connectivity.

        old_vertices: vertices of the main graph which are not in new vertices.

        new_vertices: new vertices to check connectivity of.

    Returns:
        connectivity status.
    """
    uf = UnionFind()

    for edge in edges:
        vertices = list(edge.vertices)
        for i in range(1, len(vertices)):
            uf.union(vertices[0], vertices[i])

    if not old_vertices:
        if not new_vertices:
            return True

        new_components = {uf.find(v) for v in new_vertices}
        return len(new_components) == 1

    old_components = {uf.find(v) for v in old_vertices}

    return all(uf.find(v) in old_components for v in new_vertices)


class VerticesConnectivity(Metrics):

    @classmethod
    def compute(
        cls, edges: list[Edge], old_vertices: set[Vertex], new_vertices: set[Vertex]
    ) -> bool:
        """Checks the connectivity of new vertices with old vertices by the edges.

        Args:
            edges: edges to check the connectivity.

            old_vertices: vertices of the main graph which are not in new vertices.

            new_vertices: new vertices to check connectivity of.

        Returns:
            connectivity status.
        """
        status = check_connectivity(edges, old_vertices, new_vertices)
        return status
