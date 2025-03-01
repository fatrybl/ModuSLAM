from dataclasses import dataclass, field


@dataclass
class BinaryConnectionParams:
    """Visualization parameters for connections."""

    label_color: str = "black"
    label_fontsize: int = 14
    label_alpha: float = 1.0
    label_offset: float = 0.05
    line_width: float = 4.0
    line_alpha: float = 1.0
    line_color: str = "gray"
    base_offset: float = 0.004
    curvature: float = 0.01


@dataclass
class UnaryConnectionParams:
    """Visualization parameters for unary connections."""

    label_color: str = "black"
    label_fontsize: int = 14
    label_offset: float = 0.01
    label_alpha: float = 1.0
    line_color: str = "gray"
    line_base_height: float = 0.05
    line_width: float = 5.0
    line_alpha: float = 1.0


@dataclass
class ClusterParams:
    """Parameters for the Cluster."""

    label_fontsize: int = 14
    cluster_label_offset: float = 0.15
    width: float = 1
    width_step: int = 1
    height: float = 0.05
    time_range_fontsize: int = 14
    time_range_label_offset: float = 0.1


@dataclass
class VertexParams:
    """Parameters for the Vertex."""

    color: str = "skyblue"
    label_fontsize: int = 14
    scale: float = 0.5


@dataclass
class VisualizationParams:
    """Parameters for the Graph Visualizer."""

    between_clusters_space: float = 1.0

    vertex_params: VertexParams = field(default_factory=VertexParams)
    cluster_params: ClusterParams = field(default_factory=ClusterParams)
    unary_connection_params: UnaryConnectionParams = field(default_factory=UnaryConnectionParams)
    binary_connection_params: BinaryConnectionParams = field(default_factory=BinaryConnectionParams)
