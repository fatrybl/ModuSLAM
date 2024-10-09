import logging
from collections.abc import Iterable
from typing import Generic

import gtsam

from moduslam.frontend_manager.graph.base_vertices import (
    BaseVertex,
    NotOptimizableVertex,
    OptimizableVertex,
    Vertex,
)
from moduslam.frontend_manager.graph.index_generator import IndexStorage
from moduslam.logger.logging_config import frontend_manager
from moduslam.utils.auxiliary_methods import equal_integers
from moduslam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class VertexStorage(Generic[BaseVertex]):
    """Stores vertices of the Graph.

    TODO: remove hardcoded table of vertices.
    """

    def __init__(self):
        self._index_storage = IndexStorage()
        self._vertices = OrderedSet[BaseVertex]()
        self._optimizable_vertices = OrderedSet[OptimizableVertex]()
        self._not_optimizable_vertices = OrderedSet[NotOptimizableVertex]()
        self._index_vertices_table: dict[int, set[Vertex]] = {}
        self._vertices_table: dict[type[BaseVertex], OrderedSet[BaseVertex]] = {}

    @property
    def index_storage(self) -> IndexStorage:
        """Storage for the indices of the vertices."""
        return self._index_storage

    @property
    def vertices(self) -> OrderedSet[BaseVertex]:
        """All vertices in the Graph."""
        return self._vertices

    @property
    def optimizable_vertices(self) -> OrderedSet[OptimizableVertex]:
        """Optimizable vertices in the Graph."""
        return self._optimizable_vertices

    @property
    def not_optimizable_vertices(self) -> OrderedSet[NotOptimizableVertex]:
        """Not optimizable vertices in the Graph."""
        return self._not_optimizable_vertices

    def find_closest_optimizable_vertex(
        self, vertex_type: type[OptimizableVertex], timestamp: int, margin: int
    ) -> OptimizableVertex | None:
        """Finds the closest optimizable vertex with the given timestamp, time margin and type.
        Start searching from the latest vertex to reduce complexity.
        Complexity: O(N).

        TODO: Implement a more efficient search algorithm.Add tests.
        Args:
            vertex_type: type of the vertex.

            timestamp: timestamp of the vertex.

            margin: time margin.

        Returns:
            vertex if found, None otherwise.
        """
        for v in reversed(self._optimizable_vertices):
            if equal_integers(v.timestamp, timestamp, margin) and isinstance(v, vertex_type):
                return v

        return None

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

    def add(self, vertex: BaseVertex | Iterable[BaseVertex]) -> None:
        """Adds vertex(s).

        Args:
            vertex: new vertex(s) to be added to the graph.
        """
        if isinstance(vertex, Iterable):
            for v in vertex:
                self._add(v)
        else:
            self._add(vertex)

    def remove(self, vertex: BaseVertex | Iterable[BaseVertex]) -> None:
        """Removes vertex(s).

        Args:
            vertex: vertex(s) to be removed from the graph.
        """
        if isinstance(vertex, Iterable):
            for v in vertex:
                self._remove(v)
        else:
            self._remove(vertex)

    def update_optimizable_vertices(self, values: gtsam.Values) -> None:
        """Updates optimizable vertices with new values.

        Args:
            values: new values for the vertices.
        """

        for vertex in self._optimizable_vertices:
            vertex.update(values)

    def update_not_optimizable_vertices(self) -> None:
        """Updates non-optimizable vertices."""
        raise NotImplementedError

    def get_last_vertex(self, vertex_type: type[BaseVertex]) -> BaseVertex | None:
        """Gets the vertex with the latest timestamp.

        Args:
            vertex_type: type of the vertex.

        Returns:
            vertex if found, None otherwise.
        """
        msg = f"Vertex of type {vertex_type.__name__!r} is not present in the storage."
        try:
            v = self.get_vertices(vertex_type)[-1]
            return v
        except IndexError:
            logger.debug(msg)
            return None
        except KeyError:
            logger.debug(msg)
            return None

    def get_vertices_with_index(self, index: int) -> list[Vertex]:
        """Gets the vertices with the given index.

        Args:
            index: index of the vertex.

        Returns:
            vertices or empty list.
        """
        return [v for v in self._vertices if v.index == index]

    def get_vertices_with_gtsam_index(self, index: int) -> list[OptimizableVertex]:
        """Gets the vertices with the given gtsam index.

        Args:
            index: GTSAM index of the vertex.

        Returns:
            vertices or empty list.
        """
        return [v for v in self._optimizable_vertices if v.backend_index == index]

    def _add_to_tables(self, vertex: BaseVertex) -> None:
        """Adds vertex to the tables:
            1. "Vertex type -> vertices" table.\n
            2. "Vertex index -> vertices" table.

        Args:
            vertex: vertex to be added to the tables.
        """
        t = type(vertex)
        if t not in self._vertices_table:
            self._vertices_table[t] = OrderedSet()

        self._vertices_table[t].add(vertex)

        if vertex.index not in self._index_vertices_table:
            self._index_vertices_table[vertex.index] = set()

        self._index_vertices_table[vertex.index].add(vertex)

    def _remove_from_tables(self, vertex: BaseVertex) -> None:
        """Removes vertex from the tables:
            1. "Vertex type -> vertices" table.\n
            2. "Vertex index -> vertices" table.

        Args:
            vertex: vertex to be removed from the tables.
        """

        t = type(vertex)

        if t in self._vertices_table and vertex in self._vertices_table[t]:
            self._vertices_table[t].remove(vertex)

        if (
            vertex.index in self._index_vertices_table
            and vertex in self._index_vertices_table[vertex.index]
        ):
            self._index_vertices_table[vertex.index].remove(vertex)

            if not self._index_vertices_table[vertex.index]:
                self._index_storage.remove(vertex.index)
                del self._index_vertices_table[vertex.index]

    def _add(self, vertex: BaseVertex) -> None:
        """Adds vertex(s).

        Args:
            vertex: new vertex(s) to be added to the graph.

        Raises:
            TypeError: if the vertex is neither Optimizable nor NotOptimizable.
        """
        self._index_storage.add(vertex.index)
        self._vertices.add(vertex)
        self._add_to_tables(vertex)

        if isinstance(vertex, OptimizableVertex):
            self._optimizable_vertices.add(vertex)
        elif isinstance(vertex, NotOptimizableVertex):
            self._not_optimizable_vertices.add(vertex)
        else:
            msg = f"Vertex {vertex!r} of type {type(vertex)!r} is neither Optimizable nor NotOptimizable."
            logger.critical(msg)
            raise TypeError(msg)

    def _remove(self, vertex: BaseVertex) -> None:
        """Removes one vertex from the graph.

        Args:
            vertex: vertex to be removed.

        Raises:
            TypeError: if the vertex is neither Optimizable nor NotOptimizable.
        """
        self._vertices.remove(vertex)
        self._remove_from_tables(vertex)

        if isinstance(vertex, OptimizableVertex):
            self._optimizable_vertices.remove(vertex)
        elif isinstance(vertex, NotOptimizableVertex):
            self._not_optimizable_vertices.remove(vertex)
        else:
            msg = f"Vertex {vertex!r} of type {type(vertex)!r} is neither Optimizable nor NotOptimizable."
            logger.critical(msg)
            raise TypeError(msg)
