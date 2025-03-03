from typing import Any, TypeVar

from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.exceptions import ItemExistsError, ItemNotExistsError

V = TypeVar("V", bound=Vertex)


class VertexCluster:
    """Stores vertices and their timestamps."""

    def __init__(self):
        self._vertex_timestamps_table: dict[Vertex, dict[int, int]] = {}
        self._t_range: TimeRange | None = None

    def __repr__(self) -> str:
        vertices = self._vertex_timestamps_table.keys()
        return f"Cluster with: {vertices}"

    def __contains__(self, item: Any) -> bool:
        """Checks if an item is in the cluster."""
        return item in self._vertex_timestamps_table

    @property
    def empty(self) -> bool:
        """Cluster empty status."""
        return not bool(self._vertex_timestamps_table)

    @property
    def vertices(self) -> tuple[Vertex, ...]:
        """Vertices in the cluster."""
        return tuple(self._vertex_timestamps_table.keys())

    @property
    def vertices_with_timestamps(self) -> dict[Vertex, dict[int, int]]:
        """Table of <Vertex - {timestamp: num_occurrences}>."""
        return self._vertex_timestamps_table

    @property
    def time_range(self) -> TimeRange:
        """Calculates the time range (start, stop) of the cluster.

        Raises:
            ValueError: If the cluster is empty.
        """
        if self._t_range:
            return self._t_range

        raise ValueError("Time range does not exist for empty cluster.")

    def add(self, vertex: Vertex, timestamp: int) -> None:
        """Adds a vertex with an associated timestamp to the cluster.

        Args:
            vertex: a vertex to add.

            timestamp: a timestamp associated with the vertex.

        Raises:
            ItemExistsError: if the vertex already exists in the cluster.
        """
        if vertex in self._vertex_timestamps_table:
            raise ItemExistsError(f"Vertex{vertex} already exists")

        self._vertex_timestamps_table[vertex] = {timestamp: 1}

        self._update_t_range_on_add(timestamp)

    def remove(self, vertex: Vertex) -> None:
        """Removes a vertex from the cluster.

        Args:
            vertex: a vertex to be removed.

        Raises:
            ItemNotExistsError: a vertex does not exist in the cluster.
        """
        if vertex not in self._vertex_timestamps_table:
            raise ItemNotExistsError(f"Vertex{vertex} does not exist so can`t be removed.")

        del self._vertex_timestamps_table[vertex]

        self._update_t_range()

    def add_timestamp(self, vertex: Vertex, timestamp: int) -> None:
        """Adds a timestamp to the vertex.

        Args:
            vertex: a vertex to add a timestamp.
            timestamp: a timestamp to add.

        Raises:
            ItemNotExistsError: if the vertex does not exist in the cluster.
        """
        try:
            t_occurences = self._vertex_timestamps_table[vertex]
            t_occurences[timestamp] = t_occurences.get(timestamp, 0) + 1
        except KeyError:
            raise ItemNotExistsError(f"Vertex {vertex} does not exist in the cluster.")

        self._update_t_range_on_add(timestamp)

    def remove_timestamp(self, vertex: Vertex, timestamp: int) -> None:
        """Removes a timestamp from the vertex.

        Args:
            vertex: a vertex to remove a timestamp.

            timestamp: a timestamp to remove.

        Raises:
            ItemNotExistsError: if the vertex does not exist in the cluster.

            ValueError: if the timestamp does not exist for the vertex.
        """
        try:
            t_occurences = self._vertex_timestamps_table[vertex]
            num = t_occurences.get(timestamp)
            if num is None:
                raise ValueError(f"Timestamp {timestamp} does not exist for vertex {vertex}.")
            if num == 1:
                del t_occurences[timestamp]
            else:
                t_occurences[timestamp] = num - 1

            if not t_occurences:
                del self._vertex_timestamps_table[vertex]

        except KeyError:
            raise ItemNotExistsError(f"Vertex {vertex} does not exist in the cluster.")

        self._update_t_range()

    def get_vertices_of_type(self, vertex_type: type[V]) -> tuple[V, ...]:
        """Returns all vertices of the specific type.

        Args:
            vertex_type: The type of vertices to retrieve.

        Returns:
             tuple with vertices of the given type.
        """
        return tuple(v for v in self._vertex_timestamps_table if type(v) is vertex_type)

    def get_vertex_of_type(self, vertex_type: type[V]) -> V | None:
        """Gets the vertex of the given type.

        Args:
            vertex_type: a type of the vertex to retrieve.

        Returns:
            the vertex or None if not exists.
        """
        try:
            v = next(v for v in self._vertex_timestamps_table if type(v) is vertex_type)
            return v

        except StopIteration:
            return None

    def get_timestamps(self, vertex: Vertex) -> list[int]:
        """Gets the timestamps of the vertex.

        Args:
            vertex: a vertex whose timestamp to retrieve.

        Returns:
            a timestamp of the vertex.

        Raises:
            ItemNotExistsError: if the vertex does not exist in the cluster.
        """
        try:
            return sorted(self._vertex_timestamps_table[vertex].keys())
        except KeyError:
            raise ItemNotExistsError(f"Vertex {vertex} does not exist in the cluster.")

    def _update_t_range_on_add(self, timestamp: int) -> None:
        """Updates the time range when a new timestamp is added.

        Args:
            timestamp: The new timestamp to add.
        """
        if self._t_range is None:
            self._t_range = TimeRange(start=timestamp, stop=timestamp)
        else:
            self._t_range.start = min(self._t_range.start, timestamp)
            self._t_range.stop = max(self._t_range.stop, timestamp)

    def _update_t_range(self) -> None:
        """Updates the time range of the cluster.

        TODO: time range recalculation takes O(n) time.
        """

        if not self._vertex_timestamps_table:
            self._t_range = None

        else:
            timestamps = [
                timestamp
                for t_occurences in self._vertex_timestamps_table.values()
                for timestamp in t_occurences.keys()
            ]

            start = min(timestamps)
            stop = max(timestamps)
            self._t_range = TimeRange(start, stop)
