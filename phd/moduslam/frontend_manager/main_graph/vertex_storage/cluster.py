from moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.external.metrics.utils import median
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex


class VertexCluster:
    """Stores vertices."""

    def __init__(self):
        self._vertices: dict[type[Vertex], list[Vertex]] = {}
        self._vertex_timestamp_table = dict[Vertex, int]()
        self._timestamps: list[int] = []

    def __repr__(self) -> str:
        types = [key for key in self._vertices.keys()]
        return f"Cluster with:{types}"

    def __contains__(self, item) -> bool:
        """
        TODO: take O(N) time complexity.
        """
        v_type = type(item)
        if v_type in self._vertices:
            vertices = self._vertices[v_type]
            return item in vertices
        else:
            return False

    def is_empty(self) -> bool:
        """Checks if the cluster is empty."""
        return not self._vertices

    @property
    def vertices(self) -> list[Vertex]:
        """All vertices."""
        return list(self._vertex_timestamp_table.keys())

    @property
    def vertices_with_timestamps(self) -> dict[Vertex, int]:
        """All vertices with timestamps."""
        return self._vertex_timestamp_table

    @property
    def timestamp(self) -> int:
        """Median timestamp of the cluster.

        Raises:
            ValueError: for empty cluster.
        """
        if self._timestamps:
            sorted_timestamps = sorted(self._timestamps)
            return median(sorted_timestamps)
        else:
            raise ValueError("Timestamp does not exist for empty cluster.")

    @property
    def time_range(self) -> TimeRange:
        """Time range of measurements inside the cluster.

        Raises:
            ValueError: for empty cluster.
        """
        if self._timestamps:
            sorted_timestamps = sorted(self._timestamps)
            start, stop = sorted_timestamps[0], sorted_timestamps[-1]
            return TimeRange(start, stop)
        else:
            raise ValueError("Time range does not exist for empty cluster.")

    def add(self, vertex: Vertex, timestamp: int) -> None:
        """Adds a vertex to the cluster with a timestamp.

        Args:
            vertex: a vertex to add.

            timestamp: a vertex timestamp.
        """
        self._vertices.setdefault(type(vertex), []).append(vertex)
        self._vertex_timestamp_table[vertex] = timestamp
        self._timestamps.append(timestamp)

    def remove(self, vertex: Vertex) -> None:
        """Removes vertex from the cluster.

        Args:
            vertex: a vertex to be removed.
        """
        timestamp = self._vertex_timestamp_table[vertex]
        self._vertices[type(vertex)].remove(vertex)
        self._vertex_timestamp_table.pop(vertex, None)
        self._timestamps.remove(timestamp)

    def get_vertices_of_type(self, vertex_type: type[Vertex]) -> list[Vertex]:
        """Returns vertices of the given type.

        Args:
            vertex_type: type of the vertices.

        Returns:
            vertices of the given type.
        """
        if vertex_type in self._vertices:
            return self._vertices[vertex_type]
        else:
            return []

    def get_latest_vertex(self, vertex_type: type[Vertex]) -> Vertex | None:
        """Gets the vertex with the latest timestamp of the given type if it exists.

        Args:
            vertex_type: a type of the vertex to find.

        Returns:
            vertex or None.
        """
        vertices_of_type = [
            vertex for vertex in self._vertex_timestamp_table if isinstance(vertex, vertex_type)
        ]

        if not vertices_of_type:
            return None

        return max(vertices_of_type, key=lambda v: self._vertex_timestamp_table[v])
