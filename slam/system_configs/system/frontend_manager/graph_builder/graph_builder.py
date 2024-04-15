from dataclasses import dataclass

from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.system_configs.system.frontend_manager.element_distributor.element_distributor import (
    ElementDistributorConfig,
)
from slam.system_configs.system.frontend_manager.graph_builder.candidate_factory.config import (
    CandidateFactoryConfig,
)
from slam.system_configs.system.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)


@dataclass
class GraphBuilderConfig:
    """Config for GraphBuilder."""

    name: str
    candidate_factory: CandidateFactoryConfig
    element_distributor: ElementDistributorConfig
    graph_merger: GraphMergerConfig
    edge_factories: dict[str, EdgeFactoryConfig]
