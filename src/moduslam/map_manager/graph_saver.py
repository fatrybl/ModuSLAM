from pathlib import Path

import gtsam
from graphviz import Source

from moduslam.frontend_manager.main_graph.graph import Graph


class GraphSaver:
    """Saves the graph."""

    def __init__(self) -> None:
        self._txt_file_path = Path("graph.txt")
        self._graphviz_formatting = gtsam.GraphvizFormatting()
        self._graphviz_formatting.paperHorizontalAxis = gtsam.GraphvizFormatting.Axis.X
        self._graphviz_formatting.paperVerticalAxis = gtsam.GraphvizFormatting.Axis.Y

    @staticmethod
    def serialize_factor_graph(
        factor_graph: gtsam.NonlinearFactorGraph, file_path: Path | None = None
    ) -> None:
        """Serializes the GTSAM factor graph into .txt file.

        Args:
            factor_graph: a GTSAM factor graph to serialize.

            file_path: a path to the file.
        """
        path = file_path if file_path else Path("serialized_graph.txt")
        graph_str = factor_graph.serialize()
        with open(path, "w") as file:
            file.write(graph_str)

    @staticmethod
    def save_to_file(graph: Graph, path: Path | None = None) -> None:
        """Saves graph to the file.

        Args:
            graph: a graph to save.

            path: a path to the file.
        """
        file = path if path else Path("graph.txt")
        backend_instances = graph.get_backend_instances()
        graph.factor_graph.saveGraph(file.as_posix(), backend_instances)

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
