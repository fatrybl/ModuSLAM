from dataclasses import dataclass, field

from omegaconf import MISSING

from configs.system.frontend_manager.element_distributor.element_distributor import (
    ElementDistributorConfig,
)
from configs.system.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)


@dataclass
class GraphBuilderConfig:
    """
    Config for GraphBuilder.
    """

    class_name: str = MISSING

    element_distributor: ElementDistributorConfig = field(default_factory=ElementDistributorConfig)

    graph_merger: GraphMergerConfig = field(default_factory=GraphMergerConfig)
