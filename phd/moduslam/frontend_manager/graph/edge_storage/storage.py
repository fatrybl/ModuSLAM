from collections import OrderedDict
from typing import Generic

from phd.moduslam.frontend_manager.graph.edges.base import BaseEdge


class EdgeStorage(Generic[BaseEdge]):
    """Stores edges of the Graph."""

    def __init__(self):
        self._counter: int = -1
        self._edges: OrderedDict[BaseEdge, int] = OrderedDict()

    @property
    def edges(self) -> OrderedDict[BaseEdge, int]:
        """Edges with the corresponding indices."""
        return self._edges

    def add(self, edge: BaseEdge) -> None:
        """Adds new edge(s).

        Args:
            edge: a new edge to be added.
        """
        self._counter += 1
        self._edges.update({edge: self._counter})

    def remove(self, edge: BaseEdge):
        """Removes edge(s).

        Args:
            edge: an edge to be removed.

        Raises:
            KeyError: if the edge is not in the EdgeStorage.
        """
        try:
            del self._edges[edge]
        except KeyError:
            raise KeyError(f"Edge {edge} is not in the EdgeStorage.")
