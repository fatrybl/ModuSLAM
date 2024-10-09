from pathlib import Path

import gtsam
from graphviz import Source

from moduslam.frontend_manager.graph.graph import Graph


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

        graph.factor_graph.saveGraph(self._path.as_posix(), graph.backend_values)

    def save_to_pdf(self, graph: Graph) -> None:
        """Saves graph to .pdf file.

        Args:
            graph: a graph to save.
        """
        dot = graph.factor_graph.dot(graph.backend_values, writer=self._graphviz_formatting)
        source = Source(dot)
        source.render("graph", format="pdf", cleanup=True)

    def view(self, graph: Graph) -> None:
        """Visualizes the .pdf file with the graph.

        Args:
            graph: a graph to visualize.
        """
        dot = graph.factor_graph.dot(graph.backend_values, writer=self._graphviz_formatting)
        source = Source(dot)
        source.view("graph", cleanup=True)
