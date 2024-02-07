from dataclasses import dataclass

from configs.system.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)


@dataclass
class PointCloudBuilderConfig(GraphBuilderConfig):
    """
    Config for PointCloudBuilder.
    """
