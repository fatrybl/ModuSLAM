import logging
from typing import Any, TypeVar

from phd.logger.logging_config import frontend_manager
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import (
    NonOptimizableVertex,
    OptimizableVertex,
    Vertex,
)
from phd.moduslam.utils.exceptions import (
    ItemExistsError,
    ItemNotFoundError,
    ValidationError,
)
from phd.moduslam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)

V = TypeVar("V", bound=Vertex)


class VertexStorage:
    """Stores vertices of the Graph."""

    def __init__(self):
        self._clusters = OrderedSet[VertexCluster]()
        self._optimizable_vertices = OrderedSet[OptimizableVertex]()
        self._non_optimizable_vertices = OrderedSet[NonOptimizableVertex]()
        self._vertices_table: dict[type[Vertex], OrderedSet] = {}
        self._indices: dict[type[Vertex], int] = {}
        self._timestamp_cluster_table: dict[int, VertexCluster] = {}

    def __contains__(self, item: Any) -> bool:
        """Checks if an item is in the storage."""
        return item in self._optimizable_vertices or item in self._non_optimizable_vertices

    @property
    def vertices(self) -> list[Vertex]:
        """All vertices.

        Complexity: O(N).
        """
        vertices = []
        for cluster in self._clusters:
            vertices.extend(cluster.vertices)

        return vertices

    @property
    def clusters(self) -> OrderedSet[VertexCluster]:
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

    def add(self, vertex: NewVertex) -> None:
        """Adds new vertex to the corresponding cluster.

        Args:
            vertex: a new vertex to add.

        Raises:
            ValidationError: if a vertex does not pass validation.

            TypeError: if a vertex is neither OptimizableVertex nor NonOptimizableVertex.
        """
        v = vertex.instance
        t = vertex.timestamp
        cluster = vertex.cluster
        v_type = type(v)

        try:
            self._validate_new_vertex(vertex)
        except ItemExistsError as e:
            logger.error(f"Validation failed: {e}")
            raise ValidationError(e)

        cluster.add(v, t)

        self._timestamp_cluster_table[t] = cluster
        self._indices.update({v_type: v.index})
        self._vertices_table.setdefault(v_type, OrderedSet()).add(v)

        self._process_cluster(cluster, self._clusters)

        if isinstance(v, OptimizableVertex):
            self._optimizable_vertices.add(v)
        elif isinstance(v, NonOptimizableVertex):
            self._non_optimizable_vertices.add(v)
        else:
            raise TypeError("A new vertex is neither OptimizableVertex nor NonOptimizableVertex")

    def remove(self, vertex: Vertex) -> None:
        """Removes vertex.

        Args:
            vertex: a vertex to be removed.

        Raises:
            TypeError: if a vertex is neither OptimizableVertex nor NonOptimizableVertex.
        """
        v_type = type(vertex)
        self._vertices_table[v_type].remove(vertex)

        cluster = self.get_vertex_cluster(vertex)
        cluster.remove(vertex)

        if cluster.empty:
            self._clusters.remove(cluster)

        if isinstance(vertex, OptimizableVertex):
            self._optimizable_vertices.remove(vertex)

        elif isinstance(vertex, NonOptimizableVertex):
            self._non_optimizable_vertices.remove(vertex)

        else:
            raise TypeError(
                "A vertex to be removed is neither OptimizableVertex nor NonOptimizableVertex"
            )

    def get_vertices(self, vertex_type: type[V]) -> OrderedSet[V]:
        """Gets vertices of the given type.

        Args:
            vertex_type: type of the vertices.

        Returns:
            vertices of the given type.
        """
        return self._vertices_table.get(vertex_type, OrderedSet())

    def get_last_vertex(self, vertex_type: type[V]) -> V | None:
        """Gets the last added vertex of the given type from the last added cluster.

        Args:
            vertex_type: type of the vertex.

        Returns:
            vertex if exists or None.
        """

        for cluster in reversed(self._clusters):
            vertex = cluster.get_last_vertex(vertex_type)
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

    def get_cluster(self, timestamp: int) -> VertexCluster | None:
        """Gets the cluster which time range includes the given timestamp.

        Args:
            timestamp: a timestamp.

        Returns:
            cluster if exists or None.
        """
        for cluster in self._clusters:
            start = cluster.time_range.start
            stop = cluster.time_range.stop
            if start <= timestamp <= stop:
                return cluster

        return None

    def get_last_index(self, vertex_type: type[Vertex]) -> int:
        """Gets the index of the last added vertex of the given type.

        Args:
            vertex_type: type of the vertex.

        Returns:
            index.

        Raises:
            KeyError: if the vertex type is not found in the indices table.
        """
        return self._indices[vertex_type]

    @staticmethod
    def _process_cluster(cluster: VertexCluster, clusters: OrderedSet[VertexCluster]) -> None:
        """Adds cluster to the clusters list.
        Complexity: O(N) in the worst case.

        Args:
            cluster: a new cluster to be added.
        """
        if cluster in clusters:
            return

        if not clusters or cluster.timestamp > clusters.last.timestamp:
            clusters.add(cluster)
            return

        for i in range(len(clusters) - 1, -1, -1):
            existing_cluster = clusters[i]
            if cluster.timestamp > existing_cluster.timestamp:
                clusters.insert(cluster, i + 1)
                return

        clusters.insert(cluster, 0)

    def _validate_new_vertex(self, vertex: NewVertex):
        """Validates a new vertex before adding.

        Args:
            vertex: a new vertex to be added.

        Raises:
            ItemExistsError:
                1. if the vertex already exists in the cluster.
                2. if a new timestamp is already included in another cluster.
        """
        t = vertex.timestamp
        cluster = vertex.cluster
        v = vertex.instance

        existing_cluster = self._timestamp_cluster_table.get(t, None)

        if v in cluster:
            raise ItemExistsError(f"Vertex{v} is already in cluster")

        if existing_cluster and existing_cluster is not cluster:
            raise ItemExistsError(f"A timestamp{t} can not belong to different clusters.")
