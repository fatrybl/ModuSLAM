from pathlib import Path

from slam.frontend_manager.graph.graph import Graph


class GraphSaver:
    """Saves the graph to the disk."""

    def __init__(self) -> None:
        self._directory: Path = Path()
        self._format: str = "interactive_slam"

    def save(self, graph: Graph) -> None:
        """Saves the graph to the disk.

        Args:
            graph (Graph): graph to save.
        """
        pass
