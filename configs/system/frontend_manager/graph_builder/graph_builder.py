from dataclasses import dataclass

from configs.system.frontend_manager.element_distributor.element_distributor import (
    ElementDistributorConfig,
)
from configs.system.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)


@dataclass
class GraphBuilderConfig:
    """Config for GraphBuilder."""

    class_name: str
    element_distributor: ElementDistributorConfig
    graph_merger: GraphMergerConfig
