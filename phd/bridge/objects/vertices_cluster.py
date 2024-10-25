from collections import defaultdict
from collections.abc import Iterable

from moduslam.frontend_manager.graph.base_vertices import Vertex
from phd.bridge.objects.merging_rules import rules


class Cluster:
    """Stores vertices belonging to the measurements of the same cluster."""

    def __init__(self):
        self._vertex2vertex_map: dict[Vertex, Vertex] = {}
        self._vertices: defaultdict[type[Vertex], list[Vertex]] = defaultdict(list)

    def add(self, vertices: Iterable[Vertex] | Vertex) -> None:
        """Adds new vertex(s) to the cluster.

        Args:
            vertices: new vertex(s) to be added.
        """

        if isinstance(vertices, Iterable):
            for vertex in vertices:
                self._vertices[type(vertex)].append(vertex)
        else:
            self._vertices[type(vertices)].append(vertices)

    def merge_vertices(self) -> None:
        """Merges vertices of the same type using the predefined rules."""
        for v_type, vertices in self._vertices.items():
            merge = rules.get(v_type)
            if merge:
                merged_vertex = merge(vertices)
                for vertex in vertices:
                    self._vertex2vertex_map[vertex] = merged_vertex

    def clear(self) -> None:
        """Clears temperary data."""
        self._vertex2vertex_map.clear()
