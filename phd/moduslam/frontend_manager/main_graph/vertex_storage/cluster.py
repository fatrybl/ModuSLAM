from typing import TypeVar

from phd.external.metrics.utils import median
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex

V = TypeVar("V", bound=Vertex)  # Method-specific vertex type for get_latest_vertex


class VertexCluster:
    """Stores vertices and their timestamps."""

    def __init__(self):
        self._vertices: dict[type, list[Vertex]] = {}
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
    def time_range(self) -> tuple[int, int]:
        """Calculates the time range (start, stop) of the cluster.

        Raises:
            ValueError: If the cluster is empty.
        """
        if self._timestamps:
            return min(self._timestamps), max(self._timestamps)
        raise ValueError("Time range does not exist for empty cluster.")

    def add(self, vertex: Vertex, timestamp: int) -> None:
        """Adds a vertex with an associated timestamp to the cluster.

        Args:
            vertex: The vertex to add.
            timestamp: The timestamp associated with the vertex.
        """
        v_type = type(vertex)
        self._vertices.setdefault(v_type, []).append(vertex)
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

    def get_latest_vertex(self, vertex_type: type[V]) -> V | None:
        """Gets the vertex of the specified type with the latest timestamp.

        Args:
            vertex_type: a type of the vertex to retrieve.

        Returns:
            The vertex with the latest timestamp or None if none exist.
        """
        vertices_of_type = [
            vertex for vertex in self._vertex_timestamp_table if isinstance(vertex, vertex_type)
        ]
        if not vertices_of_type:
            return None
        return max(vertices_of_type, key=lambda v: self._vertex_timestamp_table[v])
