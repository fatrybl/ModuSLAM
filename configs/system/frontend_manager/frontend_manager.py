from dataclasses import dataclass, field

from configs.system.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)


@dataclass
class FrontendManagerConfig:
    """
    Config for FrontendManager.
    """

    graph_builder: GraphBuilderConfig = field(default_factory=GraphBuilderConfig)
