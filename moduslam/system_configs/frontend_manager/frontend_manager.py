from dataclasses import dataclass

from moduslam.system_configs.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)
from moduslam.system_configs.frontend_manager.graph_initializer.prior import (
    GraphInitializerConfig,
)


@dataclass
class FrontendManagerConfig:
    """Base frontend manager configuration."""

    graph_builder: GraphBuilderConfig
    graph_initializer: GraphInitializerConfig | None = None
