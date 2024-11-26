from typing import TypeVar

from phd.external.metrics.utils import median
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.ordered_set import OrderedSet

V = TypeVar("V", bound=Vertex)


class VertexCluster:
    """Stores vertices and their timestamps."""

    def __init__(self):
        self._vertices: dict[type, OrderedSet] = {}
        self._vertex_timestamp_table: dict[Vertex, int] = {}
        self._timestamps: list[int] = []

    def __repr__(self) -> str:
        types = list(self._vertices.keys())
        return f"Cluster with types: {types}"

    def __contains__(self, item: Vertex) -> bool:
        """Checks if a vertex is in the cluster."""
        v_type = type(item)
        return item in self._vertices.get(v_type, [])

    def is_empty(self) -> bool:
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
        """
        v_type = type(vertex)
        self._vertices.setdefault(v_type, OrderedSet()).add(vertex)
        self._vertex_timestamp_table[vertex] = timestamp
        self._timestamps.append(timestamp)

    def remove(self, vertex: Vertex) -> None:
        """Removes a vertex from the cluster.

        Args:
            vertex: The vertex to be removed.
        """
        v_type = type(vertex)
        self._vertices[v_type].remove(vertex)
        del self._vertex_timestamp_table[vertex]
        self._timestamps.remove(self._vertex_timestamp_table[vertex])

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
            the last added vertex or None if none exist.
        """
        try:
            return self._vertices[vertex_type].last

        except KeyError:
            return None
