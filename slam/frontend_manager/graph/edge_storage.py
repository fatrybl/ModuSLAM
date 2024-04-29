from collections.abc import Iterable
from typing import Generic, overload

from plum import dispatch

from slam.frontend_manager.graph.base_edges import GraphEdge


class EdgeStorage(Generic[GraphEdge]):
    """Stores edges of the Graph."""

    def __init__(self):
        self._edges = set[GraphEdge]()

    @property
    def edges(self) -> set[GraphEdge]:
        """Edges in the storage."""
        return self._edges

    @overload
    def add(self, edge: GraphEdge):
        """
        @overload.

        Adds new edge to the graph.

        Args:
            edge (GraphEdge): edge to be added to the graph.
        """
        self._edges.add(edge)

    @overload
    def add(self, edge: Iterable[GraphEdge]):
        """
        @overload.

        Adds new edges to the graph.

        Args:
            edge (Iterable[GraphEdge]): multiple edges to be added to the graph.
        """
        [self.add(e) for e in edge]

    @dispatch
    def add(self, edge=None):
        """
        @overload.

        Calls:
            1.  Adds new edge to the graph.

                Args:
                    edge (GraphEdge): edge to be added to the graph.

            2.  Adds new edges to the graph.

                Args:
                    edge (Iterable[GraphEdge]): multiple edges to be added to the graph.
        """

    @overload
    def remove(self, edge: GraphEdge):
        """
        @overload.

        Removes edge from the graph.

        Args:
            edge (GraphEdge): edge to be removed from the graph.
        """
        self._edges.remove(edge)

    @overload
    def remove(self, edge: Iterable[GraphEdge]):
        """
        @overload.

        Removes multiple edges from the graph.

        Args:
            edge (Iterable[GraphEdge]): multiple edges to be removed from the graph.
        """
        [self.remove(e) for e in edge]

    @dispatch
    def remove(self, edge=None):
        """
        @overload.

        Calls:
            1.  Removes edge from the graph.

                Args:
                    edge (GraphEdge): edge to be removed from the graph.

            2.  Removes multiple edges from the graph.

                Args:
                    edge (Iterable[GraphEdge]): multiple edges to be removed from the graph.
        """
