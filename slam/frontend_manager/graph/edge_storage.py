from typing import Generic, Iterable, overload

from plum import dispatch

from slam.frontend_manager.graph.edges import GraphEdge


class EdgeStorage(Generic[GraphEdge]):
    """
    Stores edges_123 of the Graph.
    """

    def __init__(self):
        self._edges = set[GraphEdge]()

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
        Adds new edges_123 to the graph.
        Args:
            edge (Iterable[GraphEdge]): multiple edges_123 to be added to the graph.
        """
        [self.add(e) for e in edge]

    @dispatch
    def add(self, edge=None):
        """
        @overload.

        Calls:
            Args:
                edge (GraphEdge): edge to be added to the graph.

            Args:
                edge (Iterable[GraphEdge]): multiple edges_123 to be added to the graph.
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
        Removes multiple edges_123 from the graph.
        Args:
            edge (Iterable[GraphEdge]): multiple edges_123 to be removed from the graph.
        """
        [self.remove(e) for e in edge]

    @dispatch
    def remove(self, edge=None):
        """
        @overload.
        """
