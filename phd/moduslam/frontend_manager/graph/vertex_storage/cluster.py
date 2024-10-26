from moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.external.metrics.utils import median
from phd.moduslam.frontend_manager.graph.vertices.base import Vertex


class VertexCluster:
    """Stores vertices.

    TODO: полная херня. Переписать всё.
            хранить вершины в словаре нельзя.
    """

    def __init__(self):
        self._vertices = dict[Vertex, int]()
        self._timestamps: list[int] = []

    def __repr__(self):
        raise NotImplementedError

    @property
    def vertices(self) -> dict[Vertex, int]:
        """Vertices with timestamps."""
        return self._vertices

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

    def get_vertices(self, vertex_type: type[Vertex]) -> Vertex | None:
        """Returns vertices of the given type."""
        # if vertex_type in self._vertices:
        #     return self._vertices[vertex_type]
        # else:
        #     return None
        raise NotImplementedError

    def add(self, vertex: Vertex, timestamp: int) -> None:
        """Adds vertex to the cluster.

        Args:
            vertex: a vertex to add.

            timestamp: a timestamp for the vertex.
        """
        self._vertices.update({vertex: timestamp})
        self._timestamps.append(timestamp)

    def remove(self, vertex: Vertex) -> None:
        """Removes vertex from the cluster.
        TODO: rewrite better.
        Args:
            vertex: a vertex to be removed.

        Raises:
            KeyError: if the vertex is not in the cluster.
        """
        self._timestamps.remove(self._vertices[vertex])
        del self._vertices[vertex]
