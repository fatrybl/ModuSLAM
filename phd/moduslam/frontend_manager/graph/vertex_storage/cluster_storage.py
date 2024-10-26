from collections.abc import Iterable

from moduslam.frontend_manager.graph.base_vertices import Vertex
from moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.frontend_manager.graph.vertex_storage.cluster import VertexCluster


class ClusterStorage:
    """Stores clusters."""

    def __init__(self):
        self._start: int | None = None
        self._stop: int | None = None
        self._clusters: list[VertexCluster] = []

    @property
    def time_range(self) -> TimeRange:
        """Min and max timestamps of elements in the storage."""
        if self._start and self._stop:
            return TimeRange(self._start, self._stop)
        else:
            raise ValueError("Time range is not defined for an empty cluster.")

    @property
    def clusters(self) -> list[VertexCluster]:
        """All clusters."""
        return self._clusters

    def add_vertex(self, vertex: Vertex) -> None:
        # t = vertex.timestamp
        # if self._start and self._stop and t > self._start and t < self._stop:
        #     existing_cluster = self._find_cluster(t)
        #     if existing_cluster:
        #         existing_cluster.add(vertex)
        #     else:
        #         idx = self._find_closest_index(t)
        #         new_cluster = VertexCluster()
        #         new_cluster.add(vertex)
        #         self._clusters = self._clusters[:ixd] + new_cluster + self._clusters[ixd + 1 :]
        #
        # elif self._start and t < self.self._start:
        #     new_cluster = VertexCluster()
        #     new_cluster.add(vertex)
        #     self._clusters = [new_cluster] + self._clusters
        #
        # elif self._stop and t > self._stop:
        #     new_cluster = VertexCluster()
        #     new_cluster.add(vertex)
        #     self._clusters.append(new_cluster)
        ...

    def add_vertices(self, vertices: Iterable[Vertex]) -> None: ...

    def remove_vertex(self, vertex: Vertex) -> None: ...

    def remove_vertices(self, vertices: Iterable[Vertex]) -> None: ...
