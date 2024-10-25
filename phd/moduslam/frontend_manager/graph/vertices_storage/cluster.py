from moduslam.frontend_manager.graph.base_vertices import Vertex
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.ordered_set import OrderedSet
from phd.external.metrics.utils import median


class VertexCluster:
    """Stores vertices related to the same timestamp.

    TODO: recompute timestamp and time ranges more efficiently.
    """

    def __init__(self):
        self._vertices: dict[type[Vertex], OrderedSet[Vertex]] = {}
        self._timestamp: int | None = None
        self._time_range: TimeRange | None = None

    def __repr__(self):
        vertices_types = [v for v in self._vertices.keys()]
        return f"Cluster:{vertices_types}"

    @property
    def vertices(self) -> dict[type[Vertex], OrderedSet[Vertex]]:
        """Vertices in the cluster.

        TODO: do we really need a dictionary here?
        """
        return self._vertices

    @property
    def timestamp(self) -> int:
        """Median timestamp of the cluster.

        Raises:
            ValueError: for empty cluster.
        """
        if self._timestamp:
            return self._timestamp
        else:
            raise ValueError("Timestamp does not exist for empty cluster.")

    @property
    def time_range(self) -> TimeRange:
        """Time range of measurements inside the cluster.

        Raises:
            ValueError: for empty cluster.
        """
        if self._time_range:
            return self._time_range
        else:
            raise ValueError("Time range does not exist for empty cluster.")

    def add(self, vertex: Vertex) -> None:
        """Adds vertex to the cluster.

        Args:
            vertex: a vertex to add.
        """
        v_type = type(vertex)
        self._vertices.setdefault(v_type, OrderedSet()).add(vertex)
        self._timestamp = self._compute_timestamp()
        self._time_range = self._compute_time_range()

    def remove(self, vertex: Vertex) -> None:
        """Removes vertex from the cluster.

        Args:
            vertex: a vertex to be removed.
        """
        v_type = type(vertex)
        if v_type in self._vertices:
            vertices = self._vertices[v_type]
            if vertex in vertices:
                vertices.remove(vertex)
                self._timestamp = self._compute_timestamp()
                self._time_range = self._compute_time_range()

                if not vertices:
                    del self._vertices[v_type]

    def _compute_timestamp(self) -> int:
        timestamps: list[int] = []
        for vertices in self._vertices.values():
            timestamps += [v.timestamp for v in vertices]
        return median(timestamps)

    def _compute_time_range(self) -> TimeRange:
        timestamps: list[int] = []
        for vertices in self._vertices.values():
            timestamps += [v.timestamp for v in vertices]

        start = min(timestamps)
        stop = max(timestamps)
        return TimeRange(start, stop)
