import bisect
import logging

from moduslam.logger.logging_config import frontend_manager
from moduslam.utils.exceptions import ItemNotFoundError
from moduslam.utils.ordered_set import OrderedSet
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import (
    NonOptimizableVertex,
    OptimizableVertex,
    Vertex,
)

logger = logging.getLogger(frontend_manager)


class VertexStorage:
    """Stores vertices of the Graph."""

    def __init__(self):
        self._vertices_table: dict[type[Vertex], OrderedSet[Vertex]] = {}
        self._indices: dict[type[Vertex], int] = {}
        self._optimizable_vertices = OrderedSet[OptimizableVertex]()
        self._non_optimizable_vertices = OrderedSet[NonOptimizableVertex]()
        self._clusters = list[VertexCluster]()

    @property
    def vertices(self) -> list[Vertex]:
        """All vertices."""
        vertices = []
        for vertex_set in self._vertices_table.values():
            vertices += list(vertex_set)
        return vertices

    @property
    def clusters(self) -> list[VertexCluster]:
        """Clusters with vertices."""
        return self._clusters

    @property
    def optimizable_vertices(self) -> OrderedSet[OptimizableVertex]:
        """Optimizable vertices."""
        return self._optimizable_vertices

    @property
    def non_optimizable_vertices(self) -> OrderedSet[NonOptimizableVertex]:
        """Non-optimizable vertices."""
        return self._non_optimizable_vertices

    def add(self, cluster: VertexCluster, vertex: Vertex, timestamp: int) -> None:
        """Adds vertex to the corresponding cluster.

        TODO: optimize complexity. Now it take O(N) time to check "in".

        Args:
            cluster: a target cluster.

            vertex: a new vertex to be added.

            timestamp: a timestamp.

        Raises:
            TypeError: if the vertex is neither Optimizable nor NonOptimizable.
        """
        v_type = type(vertex)
        new_index = self._indices.get(v_type, -1) + 1
        vertex.index = new_index
        self._indices.update({v_type: new_index})

        cluster.add(vertex, timestamp)

        self._vertices_table[v_type].add(vertex)

        if cluster not in self._clusters:
            self._add_cluster(cluster)

        if isinstance(vertex, OptimizableVertex):
            self._optimizable_vertices.add(vertex)
        elif isinstance(vertex, NonOptimizableVertex):
            self._non_optimizable_vertices.add(vertex)
        else:
            raise TypeError(f"Invalid vertex type: {type(vertex)}")

    def remove(self, vertex: Vertex) -> None:
        """Removes vertex.

        Args:
            vertex: a vertex to be removed.

        Raises:
            TypeError: if the vertex is neither Optimizable nor NonOptimizable.
        """
        v_type = type(vertex)
        self._vertices_table[v_type].remove(vertex)

        cluster = self.get_vertex_cluster(vertex)
        cluster.remove(vertex)

        if cluster.is_empty():
            self._clusters.remove(cluster)

        if isinstance(vertex, OptimizableVertex):
            self._optimizable_vertices.remove(vertex)
        elif isinstance(vertex, NonOptimizableVertex):
            self._non_optimizable_vertices.remove(vertex)
        else:
            raise TypeError(f"Invalid vertex type: {type(vertex)}")

    def get_vertices(self, vertex_type: type[Vertex]) -> OrderedSet[Vertex]:
        """Gets vertices of the given type.

        Args:
            vertex_type: type of the vertices.

        Returns:
            vertices of the given type.
        """
        if vertex_type not in self._vertices_table:
            return OrderedSet[Vertex]()
        else:
            return self._vertices_table[vertex_type]

    def get_latest_vertex(self, vertex_type: type[Vertex]) -> Vertex | None:
        """Gets the vertex of the given type with the latest timestamp.

        Args:
            vertex_type: type of the vertex.

        Returns:
            vertex if exists or None.

        TODO: complexity: O(N^2).
        """

        for cluster in reversed(self._clusters):
            vertex = cluster.get_latest_vertex(vertex_type)
            if vertex:
                return vertex
        return None

    def get_vertex_cluster(self, vertex: Vertex) -> VertexCluster:
        """Returns the cluster that contains the given vertex.

        Args:
            vertex: a vertex.

        Returns:
            cluster.
        """

        for cluster in self._clusters:
            if vertex in cluster:
                return cluster

        logger.critical(f"Vertex {vertex} not found in any cluster.")
        raise ItemNotFoundError

    def _add_cluster(self, cluster: VertexCluster) -> None:
        """Adds cluster to the clusters list.
        Complexity: O(log N) + O(N).

        Args:
            cluster: a new cluster to be added.
        """
        timestamps = [cluster.timestamp for cluster in self._clusters]
        index = bisect.bisect_left(timestamps, cluster.timestamp)
        self._clusters.insert(index, cluster)
