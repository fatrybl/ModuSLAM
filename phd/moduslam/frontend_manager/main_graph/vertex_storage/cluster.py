from typing import Any, TypeVar

from phd.external.metrics.utils import median
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.exceptions import ItemExistsError, ItemNotExistsError
from phd.moduslam.utils.ordered_set import OrderedSet

V = TypeVar("V", bound=Vertex)


class VertexCluster:
    """Stores vertices and their timestamps."""

    def __init__(self):
        self._vertices: dict[type[Vertex], OrderedSet] = {}
        self._vertex_timestamp_table: dict[Vertex, int] = {}
        self._timestamps: list[int] = []

    def __repr__(self) -> str:
        types = list(self._vertices.keys())
        return f"Cluster with types: {types}"

    def __contains__(self, item: Any) -> bool:
        """Checks if a vertex is in the cluster."""
        return item in self._vertex_timestamp_table

    @property
    def empty(self) -> bool:
        """Checks if the cluster is empty."""
        return not bool(self._vertices)

    @property
    def vertices(self) -> list[Vertex]:
        """Returns all vertices in the cluster."""
        return list(self._vertex_timestamp_table.keys())

    @property
    def vertices_with_timestamps(self) -> dict[Vertex, int]:
        """Returns all vertices with their timestamps."""
        return self._vertex_timestamp_table

    @property
    def timestamp(self) -> int:
        """Calculates the median timestamp of the cluster.

        Raises:
            ValueError: If the cluster is empty.
        """
        if self._timestamps:
            return median(self._timestamps)

        raise ValueError("Timestamp does not exist for empty cluster.")

    @property
    def time_range(self) -> TimeRange:
        """Calculates the time range (start, stop) of the cluster.

        Raises:
            ValueError: If the cluster is empty.
        """
        if self._timestamps:
            start = min(self._timestamps)
            stop = max(self._timestamps)
            return TimeRange(start, stop)

        raise ValueError("Time range does not exist for empty cluster.")

    def add(self, vertex: Vertex, timestamp: int) -> None:
        """Adds a vertex with an associated timestamp to the cluster.

        Args:
            vertex: a vertex to add.

            timestamp: a timestamp associated with the vertex.

        Raises:
            ItemExistsError: if the vertex already exists in the cluster.
        """
        v_type = type(vertex)

        if vertex in self._vertex_timestamp_table:
            raise ItemExistsError(f"Vertex{vertex} already exists")

        self._vertex_timestamp_table[vertex] = timestamp
        self._vertices.setdefault(v_type, OrderedSet()).add(vertex)
        self._timestamps.append(timestamp)

    def remove(self, vertex: Vertex) -> None:
        """Removes a vertex from the cluster.

        Args:
            vertex: a vertex to be removed.

        Raises:
            ItemNotExistsError: a vertex does not exist in the cluster.
        """
        v_type = type(vertex)
        if vertex not in self._vertex_timestamp_table:
            raise ItemNotExistsError(f"Vertex{vertex} does not exist")

        t = self._vertex_timestamp_table[vertex]
        self._timestamps.remove(t)
        self._vertices[v_type].remove(vertex)
        del self._vertex_timestamp_table[vertex]
        if not self._vertices[v_type]:
            del self._vertices[v_type]

    def get_vertices_of_type(self, vertex_type: type[V]) -> list[V]:
        """Returns all vertices of a specific type.

        Args:
            vertex_type: The type of vertices to retrieve.

        Returns:
            A list of vertices of the given type.
        """
        return [v for v in self._vertex_timestamp_table if isinstance(v, vertex_type)]

    def get_last_vertex(self, vertex_type: type[V]) -> V | None:
        """Gets the last added vertex of the specified type.

        Args:
            vertex_type: a type of the vertex to retrieve.

        Returns:
            the last added vertex or None if not exists.
        """
        try:
            return self._vertices[vertex_type].last

        except KeyError:
            return None
