from dataclasses import dataclass, field


@dataclass
class BinaryConnectionParams:
    """Visualization parameters for connections."""

    curve_color: str = "gray"
    label_color: str = "black"
    label_fontsize: int = 16
    curve_lw: float = 2
    curve_alpha: float = 1.0
    label_alpha: float = 1.0
    label_offset: float = 0.2
    base_offset: float = 0.07


@dataclass
class UnaryConnectionParams:
    """Visualization parameters for unary connections."""

    line_color: str = "gray"
    label_color: str = "black"
    label_fontsize: int = 16
    line_spacing: float = 2
    line_width: float = 1.0
    line_alpha: float = 1.0
    label_offset: float = 0.2
    label_alpha: float = 1.0


@dataclass
class ClusterParams:
    """Parameters for the Cluster."""

    width_step: int = 7
    label_fontsize: int = 16
    label_offset: float = 10
    width: float = 7.0
    height: float = 5.0


@dataclass
class VertexParams:
    """Parameters for the Vertex."""

    color: str = "skyblue"
    label_fontsize: int = 16
    label_offset: float = 0.2


@dataclass
class VisualizationParams:
    """Parameters for the Graph Visualizer."""

    title_font_size: int = 30
    title_padding: float = 50
    between_clusters_space: float = 5

    vertex_params: VertexParams = field(default_factory=VertexParams)
    cluster_params: ClusterParams = field(default_factory=ClusterParams)
    unary_connection_params: UnaryConnectionParams = field(default_factory=UnaryConnectionParams)
    binary_connection_params: BinaryConnectionParams = field(default_factory=BinaryConnectionParams)
