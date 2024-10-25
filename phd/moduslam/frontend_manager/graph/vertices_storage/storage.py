import logging
from typing import Generic

from moduslam.frontend_manager.graph.index_generator import IndexStorage
from moduslam.logger.logging_config import frontend_manager
from moduslam.utils.ordered_set import OrderedSet
from phd.moduslam.frontend_manager.graph.vertices.base import (
    BaseVertex,
    NotOptimizableVertex,
    OptimizableVertex,
)
from phd.moduslam.frontend_manager.graph.vertices_storage.cluster import VertexCluster

logger = logging.getLogger(frontend_manager)


class VertexStorage(Generic[BaseVertex]):
    """Stores vertices of the Graph."""

    def __init__(self):
        self._vertices_table: dict[type[BaseVertex], OrderedSet[BaseVertex]] = {}
        self._index_storages: dict[type[BaseVertex], IndexStorage] = {}
        self._optimizable_vertices = OrderedSet[OptimizableVertex]()
        self._not_optimizable_vertices = OrderedSet[NotOptimizableVertex]()
        self._clusters: list[VertexCluster] = []

    @property
    def vertices(self) -> list[BaseVertex]:
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
    def index_storages(self) -> dict[type[BaseVertex], IndexStorage]:
        """Storage for the indices of the vertices."""
        return self._index_storages

    @property
    def optimizable_vertices(self) -> OrderedSet[OptimizableVertex]:
        """Optimizable vertices."""
        return self._optimizable_vertices

    @property
    def not_optimizable_vertices(self) -> OrderedSet[NotOptimizableVertex]:
        """Not optimizable vertices."""
        return self._not_optimizable_vertices

    def add(self, vertex: BaseVertex) -> None:
        """Adds vertex.

        Args:
            vertex: a new vertex to be added.
        """
        raise NotImplementedError

    def remove(self, vertex: BaseVertex) -> None:
        """Removes vertex.

        Args:
            vertex: a vertex to be removed.
        """
        raise NotImplementedError

    def get_vertices(self, vertex_type: type[BaseVertex]) -> OrderedSet[BaseVertex]:
        """Gets vertices of the given type.

        Args:
            vertex_type: type of the vertices.

        Returns:
            vertices of the given type.
        """
        if vertex_type not in self._vertices_table:
            return OrderedSet[BaseVertex]()
        else:
            return self._vertices_table[vertex_type]

    def get_latest_vertex(self, vertex_type: type[BaseVertex]) -> BaseVertex | None:
        """Gets the vertex with the latest timestamp.

        Args:
            vertex_type: type of the vertex.

        Returns:
            vertex if found, None otherwise.
        """
        vertice = self.get_vertices(vertex_type)
        if len(vertice) != 0:
            return vertice.last
        else:
            return None

    def _add(self, vertex: BaseVertex) -> None:
        """Adds vertex(s).

        Args:
            vertex: new vertex(s) to be added to the graph.

        Raises:
            TypeError: if the vertex is neither Optimizable nor NotOptimizable.
        """
        # self._index_storage.add(vertex.index)
        # self._vertices.add(vertex)
        # self._add_to_tables(vertex)
        #
        # if isinstance(vertex, OptimizableVertex):
        #     self._optimizable_vertices.add(vertex)
        # elif isinstance(vertex, NotOptimizableVertex):
        #     self._not_optimizable_vertices.add(vertex)
        # else:
        #     msg = f"Vertex {vertex!r} of type {type(vertex)!r} is neither Optimizable nor NotOptimizable."
        #     logger.critical(msg)
        #     raise TypeError(msg)
        ...

    def _add_to_tables(self, vertex: BaseVertex) -> None:
        # """Adds vertex to the tables:
        #     1. "Vertex type -> vertices" table.\n
        #     2. "Vertex index -> vertices" table.
        #
        # Args:
        #     vertex: vertex to be added to the tables.
        # """
        # t = type(vertex)
        # if t not in self._vertices_table:
        #     self._vertices_table[t] = OrderedSet()
        #
        # self._vertices_table[t].add(vertex)
        #
        # if vertex.index not in self._index_vertices_table:
        #     self._index_vertices_table[vertex.index] = set()
        #
        # self._index_vertices_table[vertex.index].add(vertex)
        ...

    def _remove_from_tables(self, vertex: BaseVertex) -> None:
        """Removes vertex from the tables:
            1. "Vertex type -> vertices" table.\n
            2. "Vertex index -> vertices" table.

        Args:
            vertex: vertex to be removed from the tables.
        """

        # t = type(vertex)
        #
        # if t in self._vertices_table and vertex in self._vertices_table[t]:
        #     self._vertices_table[t].remove(vertex)
        #
        # if (
        #     vertex.index in self._index_vertices_table
        #     and vertex in self._index_vertices_table[vertex.index]
        # ):
        #     self._index_vertices_table[vertex.index].remove(vertex)
        #
        #     if not self._index_vertices_table[vertex.index]:
        #         self._index_storage.remove(vertex.index)
        #         del self._index_vertices_table[vertex.index]
        ...

    def _remove(self, vertex: BaseVertex) -> None:
        """Removes one vertex from the graph.

        Args:
            vertex: vertex to be removed.

        Raises:
            TypeError: if the vertex is neither Optimizable nor NotOptimizable.
        """
        # self._vertices.remove(vertex)
        # self._remove_from_tables(vertex)
        #
        # if isinstance(vertex, OptimizableVertex):
        #     self._optimizable_vertices.remove(vertex)
        # elif isinstance(vertex, NotOptimizableVertex):
        #     self._not_optimizable_vertices.remove(vertex)
        # else:
        #     msg = f"Vertex {vertex!r} of type {type(vertex)!r} is neither Optimizable nor NotOptimizable."
        #     logger.critical(msg)
        #     raise TypeError(msg)
        ...
