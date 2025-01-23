from pathlib import Path

import gtsam
from graphviz import Source

from src.moduslam.frontend_manager.main_graph.graph import Graph


class GraphSaver:
    """Saves the graph."""

    def __init__(self) -> None:
        self._path: Path = Path("graph.txt")
        self._graphviz_formatting = gtsam.GraphvizFormatting()
        self._graphviz_formatting.paperHorizontalAxis = gtsam.GraphvizFormatting.Axis.X
        self._graphviz_formatting.paperVerticalAxis = gtsam.GraphvizFormatting.Axis.Y

    def save_to_file(self, graph: Graph) -> None:
        """Saves graph to the file.

        Args:
            graph: a graph to save.
        """
        backend_instances = graph.get_backend_instances()
        graph_str = graph.factor_graph.serialize()
        with open("serialized.txt", "w") as file:
            file.write(graph_str)
        graph.factor_graph.saveGraph(self._path.as_posix(), backend_instances)

    def save_to_pdf(self, graph: Graph, name: str = "graph") -> None:
        """Saves graph to .pdf file.

        Args:
            graph: a graph to save.

            name: a name for the pdf file.
        """
        backend_instances = graph.get_backend_instances()
        dot = graph.factor_graph.dot(backend_instances, writer=self._graphviz_formatting)
        source = Source(dot)
        source.render(name, format="pdf", cleanup=True)

    def save_and_view(self, graph: Graph) -> None:
        """Visualizes the .pdf file with the graph.

        Args:
            graph: a graph to visualize.
        """
        backend_instances = graph.get_backend_instances()
        dot = graph.factor_graph.dot(backend_instances, writer=self._graphviz_formatting)
        source = Source(dot)
        source.view("graph", cleanup=True)
