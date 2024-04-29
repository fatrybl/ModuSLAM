from dataclasses import dataclass

from slam.system_configs.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)
from slam.system_configs.frontend_manager.graph_initializer.prior import (
    GraphInitializerConfig,
)


@dataclass
class FrontendManagerConfig:
    """Base frontend manager configuration."""

    graph_builder: GraphBuilderConfig
    graph_initializer: GraphInitializerConfig | None = None
