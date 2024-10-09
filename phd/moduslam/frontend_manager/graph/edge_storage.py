from collections.abc import Iterable
from typing import Generic

from moduslam.frontend_manager.graph.base_edges import BaseEdge
from moduslam.utils.ordered_set import OrderedSet


class EdgeStorage(Generic[BaseEdge]):
    """Stores edges of the Graph."""

    def __init__(self):
        self._edges = OrderedSet[BaseEdge]()

    @property
    def edges(self) -> OrderedSet[BaseEdge]:
        """Edges in the storage."""
        return self._edges

    def add(self, edge: BaseEdge | Iterable[BaseEdge]):
        """Adds new edge(s).

        Args:
            edge: edge(s) to be added.
        """
        if isinstance(edge, Iterable):
            for e in edge:
                self._edges.add(e)
        else:
            self._edges.add(edge)

    def remove(self, edge: BaseEdge | Iterable[BaseEdge]):
        """Removes edge(s).

        Args:
            edge: edge(s) to be removed.
        """
        if isinstance(edge, Iterable):
            for e in edge:
                self._edges.remove(e)
        else:
            self._edges.remove(edge)
