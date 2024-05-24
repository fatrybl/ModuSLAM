from collections.abc import Iterable
from typing import Generic

from moduslam.frontend_manager.graph.base_edges import GraphEdge


class EdgeStorage(Generic[GraphEdge]):
    """Stores edges of the Graph."""

    def __init__(self):
        self._edges = set[GraphEdge]()

    @property
    def edges(self) -> set[GraphEdge]:
        """Edges in the storage."""
        return self._edges

    def add(self, edge: GraphEdge | Iterable[GraphEdge]):
        """Adds new edge(s).

        Args:
            edge: edge(s) to be added.
        """
        if isinstance(edge, Iterable):
            for e in edge:
                self._edges.add(e)
        else:
            self._edges.add(edge)

    def remove(self, edge: GraphEdge | Iterable[GraphEdge]):
        """Removes edge(s).

        Args:
            edge: edge(s) to be removed.
        """
        if isinstance(edge, Iterable):
            for e in edge:
                self._edges.remove(e)
        else:
            self._edges.remove(edge)
