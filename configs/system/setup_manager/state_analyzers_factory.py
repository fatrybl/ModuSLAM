from dataclasses import dataclass

from omegaconf import MISSING

from configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


@dataclass
class StateAnalyzersFactoryConfig:
    """
    Config for HandlerFactory.
    """

    package_name: str = MISSING
    analyzers: list[StateAnalyzerConfig] = MISSING
