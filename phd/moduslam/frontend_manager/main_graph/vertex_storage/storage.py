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
from phd.utils.exceptions import ItemExistsError, ItemNotExistsError, ValidationError
from phd.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)

V = TypeVar("V", bound=Vertex)


class VertexStorage:
    """Stores vertices of the Graph."""

    def __init__(self):
        self._clusters = OrderedSet[VertexCluster]()
        self._optimizable_vertices = OrderedSet[OptimizableVertex]()
        self._non_optimizable_vertices = OrderedSet[NonOptimizableVertex]()
        self._type_vertices_table: dict[type[Vertex], OrderedSet] = {}
        self._vertex_cluster_table: dict[Vertex, VertexCluster] = {}
        self._timestamp_cluster_table: dict[int, VertexCluster] = {}

    def __contains__(self, item: Any) -> bool:
        """Checks if an item is in the storage."""
        return item in self._vertex_cluster_table

    @property
    def vertices(self) -> list[Vertex]:
        """All vertices.

        Complexity: O(N).
        """
        return list(self._vertex_cluster_table.keys())

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
        try:
            self._validate_new_vertex(vertex)
        except ItemExistsError as e:
            logger.error(f"Validation failed: {e}")
            raise ValidationError(e)

        v = vertex.instance
        v_type = type(v)
        t = vertex.timestamp
        cluster = vertex.cluster

        cluster.add(v, t)
        self._timestamp_cluster_table[t] = cluster
        self._vertex_cluster_table[v] = cluster
        self._type_vertices_table.setdefault(v_type, OrderedSet()).add(v)
        self._process_cluster(cluster, self._clusters)

        if isinstance(v, OptimizableVertex):
            self._optimizable_vertices.add(v)
        elif isinstance(v, NonOptimizableVertex):
            self._non_optimizable_vertices.add(v)
        else:
            msg = f"Vertex {vertex!r} of type {type(vertex)!r} is neither Optimizable nor NonOptimizable."
            logger.error(msg)
            raise TypeError(msg)

    def remove(self, vertex: Vertex) -> None:
        """Removes vertex.

        Args:
            vertex: a vertex to be removed.

        Raises:
            ValidationError: if a validation has failed.
        """
        try:
            self._validate_removal_vertex(vertex)
        except ItemNotExistsError as e:
            logger.error(f"Validation failed: {e}")
            raise ValidationError(e)

        v_type = type(vertex)
        cluster = self._vertex_cluster_table[vertex]
        timestamp = cluster.get_timestamp(vertex)

        self._type_vertices_table[v_type].remove(vertex)
        del self._vertex_cluster_table[vertex]

        cluster.remove(vertex)
        if cluster.empty:
            self._clusters.remove(cluster)

        if not cluster.timestamp_exists(timestamp):
            del self._timestamp_cluster_table[timestamp]

        if isinstance(vertex, OptimizableVertex):
            self._optimizable_vertices.remove(vertex)

        if isinstance(vertex, NonOptimizableVertex):
            self._non_optimizable_vertices.remove(vertex)

        if len(self._clusters) > len(self.vertices):
            raise ValueError("The number of clusters bigger than the number of vertices.")

    def get_vertices(self, vertex_type: type[V]) -> OrderedSet[V]:
        """Gets vertices of the given type.

        Args:
            vertex_type: type of the vertices.

        Returns:
            vertices of the given type.
        """
        return self._type_vertices_table.get(vertex_type, OrderedSet[V]())

    def get_last_vertex(self, vertex_type: type[V]) -> V | None:
        """Gets the last added vertex of the given type.

        Args:
            vertex_type: type of the vertex.

        Returns:
            vertex if exists or None.
        """
        try:
            return self._type_vertices_table[vertex_type].last
        except KeyError:
            return None

    def get_vertex_cluster(self, vertex: Vertex) -> VertexCluster | None:
        """Gets the cluster that contains the given vertex.

        Args:
            vertex: a vertex to get a cluster for.

        Returns:
            cluster if exists or None.
        """
        try:
            return self._vertex_cluster_table[vertex]
        except KeyError:
            return None

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

    def get_last_index(self, vertex_type: type[Vertex]) -> int | None:
        """Gets the index of the last added vertex of the given type.

        Args:
            vertex_type: type of the vertex.

        Returns:
            index if exists or None.
        """
        try:
            item = self._type_vertices_table[vertex_type].last
            return item.index

        except KeyError:
            return None

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
        existing_cluster = self._timestamp_cluster_table.get(t, None)

        if vertex.instance in self._vertex_cluster_table:
            raise ItemExistsError(f"Vertex{vertex} already exists in the cluster.")

        if existing_cluster and existing_cluster is not vertex.cluster:
            raise ItemExistsError(f"A timestamp{t} can not belong to different clusters.")

    def _validate_removal_vertex(self, vertex: Vertex) -> None:
        """Validates a vertex to be removed.

        Args:
            vertex: a vertex to be removed.

        Raises:
            ItemNotExistsError: if the vertex does not exist in one of containers.
        """
        v_type = type(vertex)
        if (
            vertex not in self._optimizable_vertices
            and vertex not in self._non_optimizable_vertices
        ):
            raise ItemNotExistsError(
                f"Vertex {vertex} is neither in optimizable vertices nor in non-optimizable."
            )

        if v_type not in self._type_vertices_table:
            raise ItemNotExistsError(f"Vertex of type{v_type } does not exist in the storage.")

        if vertex not in self._vertex_cluster_table:
            raise ItemNotExistsError(f"Vertex {vertex} is not in the storage.")
