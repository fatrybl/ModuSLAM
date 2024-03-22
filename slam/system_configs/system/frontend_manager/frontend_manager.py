from dataclasses import dataclass

from slam.system_configs.system.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)


@dataclass
class FrontendManagerConfig:
    """Config for FrontendManager."""

    graph_builder: GraphBuilderConfig
