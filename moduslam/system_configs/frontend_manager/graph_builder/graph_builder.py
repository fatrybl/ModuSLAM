from dataclasses import dataclass

from moduslam.system_configs.frontend_manager.element_distributor.element_distributor import (
    ElementDistributorConfig,
)
from moduslam.system_configs.frontend_manager.graph_builder.candidate_factory.config import (
    CandidateFactoryConfig,
)
from moduslam.system_configs.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)


@dataclass
class GraphBuilderConfig:
    """Base GraphBuilder configuration."""

    name: str
    candidate_factory: CandidateFactoryConfig
    element_distributor: ElementDistributorConfig
    graph_merger: GraphMergerConfig
