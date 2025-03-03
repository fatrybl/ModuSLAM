from dataclasses import dataclass

from src.moduslam.map_manager.visualizers.graph_visualizer.cluster import Cluster


@dataclass
class Unary:
    """Attaches to a cluster.

    Args:
        source: a source cluster

        label: a label of the edge.
    """

    source: Cluster
    label: str

    def __repr__(self) -> str:
        return f"{self.label} to {self.source}"


@dataclass
class Binary:
    """Connects 2 clusters.

    Args:
        source: a source cluster.

        target: a target cluster.

        label: a label of the edge.
    """

    source: Cluster
    target: Cluster
    label: str
    draw_below: bool = False

    def __repr__(self) -> str:
        return f"{self.label} from {self.source} to {self.target}"
