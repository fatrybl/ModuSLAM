from src.measurement_storage.measurements.base import Measurement
from src.moduslam.frontend_manager.main_graph.data_classes import GraphElement
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.utils.ordered_set import OrderedSet


class Factory:
    """Simple factory to expand the graph with new vertices & edges."""

    def __init__(self): ...

    def expand_graph(
        self, graph: Graph, data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> Graph:
        """Creates new vertices & edges for the graph using the measurements from the data.

        Args:
            graph: a graph to expand with new vertices & edges.

            data: a table of measurements to create new edges.

        Returns:
            a new graph.
        """

        for measurement_type, measurements in data.items():
            new_elements = self.create_graph_elements(graph, measurement_type, measurements)
            graph.add_elements(new_elements)

        return graph

    @staticmethod
    def create_graph_elements(
        graph: Graph, m_type: type[Measurement], measurements: OrderedSet[Measurement]
    ) -> list[GraphElement]:
        """Creates new vertices & edges for the graph using the measurements.

        Args:
            graph: a graph to create new elements for.

            m_type: a type of the measurements.

            measurements: an ordered set of measurements.

        Returns:
            a list of new graph elements.
        """
        elements: list[GraphElement] = []

        return elements
