import logging

from slam.frontend_manager.graph.graph import Graph
from slam.map_manager.graph_saver import GraphSaver

logger = logging.getLogger(__name__)


class MapManager:
    """Manages the map."""

    def __init__(self) -> None:
        self.graph_saver = GraphSaver()

    def save_graph(self, graph: Graph) -> None:
        """Saves the graph to the disk.

        Args:
            graph (Graph): graph to save.
        """
        self.graph_saver.save(graph)
        logger.info("Graph has been saved.")
