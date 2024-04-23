from pathlib import Path

import gtsam
from graphviz import Source

from slam.frontend_manager.graph.graph import Graph


class GraphSaver:
    """Saves the graph to the disk."""

    def __init__(self) -> None:
        self._path: Path = Path("graph.txt")
        self._graphviz_formatting = gtsam.GraphvizFormatting()
        self._graphviz_formatting.paperHorizontalAxis = gtsam.GraphvizFormatting.Axis.X
        self._graphviz_formatting.paperVerticalAxis = gtsam.GraphvizFormatting.Axis.Y

    def save_to_file(self, graph: Graph) -> None:
        """Saves the graph to the disk.

        Args:
            graph (Graph): graph to save.
        """

        graph.factor_graph.saveGraph(self._path.as_posix(), graph.gtsam_values)

    def save_to_pdf(self, graph: Graph, visualize: bool = False) -> None:
        """Saves to pdf.

        Args:
            graph (Graph): graph to save.
            visualize (bool): visualize the pdf file.
        """
        dot = graph.factor_graph.dot(graph.gtsam_values, writer=self._graphviz_formatting)
        viz = Source(dot)
        viz.render("graph", format="pdf", cleanup=True)
        if visualize:
            viz.view(cleanup=True)

    def view(self, graph: Graph) -> None:
        """Visualizes the graph.

        Args:
            graph (Graph): graph to visualize.
        """
        dot = graph.factor_graph.dot(graph.gtsam_values, writer=self._graphviz_formatting)
        viz = Source(dot)
        viz.view(cleanup=True)
