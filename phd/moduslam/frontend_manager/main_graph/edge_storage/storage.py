from moduslam.utils.ordered_set import OrderedSet
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge


class EdgeStorage:
    """Stores edges of the Graph."""

    def __init__(self):
        self._edges = OrderedSet[Edge]()

    def __contains__(self, item) -> bool:
        return item in self._edges

    @property
    def edges(self) -> OrderedSet[Edge]:
        """Edges with the corresponding indices."""
        return self._edges

    def add(self, edge: Edge) -> None:
        """Adds new edge.

        Args:
            edge: a new edge to be added.
        """
        self._edges.add(edge)

    def remove(self, edge: Edge):
        """Removes edge.

        Args:
            edge: an edge to be removed.
        """
        self._edges.remove(edge)
