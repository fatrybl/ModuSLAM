from typing import Generic, Iterable

from plum import dispatch, overload

from slam.frontend_manager.graph.edges.edges import GraphEdge


class EdgeStorage(Generic[GraphEdge]):
    """
    Stores edges of the Graph.

    TODO: think about how to store edges: heap maybe?.
          as it should delete edges fast.
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
    def add(self, edges: Iterable[GraphEdge]):
        """
        @overload.
        Adds new edges to the graph.
        Args:
            edges (Iterable[GraphEdge]): multiple edges to be added to the graph.
        """
        [self.add(e) for e in edges]

    @dispatch
    def add(self, edge=None):
        """
        @overload.
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
    def remove(self, edges: Iterable[GraphEdge]):
        """
        @overload.
        Removes multiple edges from the graph.
        Args:
            edges (Iterable[GraphEdge]): multiple edges to be removed from the graph.
        """
        [self.remove(e) for e in edges]

    @dispatch
    def remove(self, edge=None):
        """
        @overload.
        """
