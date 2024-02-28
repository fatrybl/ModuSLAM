from dataclasses import dataclass

from system_configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


@dataclass
class StateAnalyzersFactoryConfig:
    """Config for HandlerFactory."""

    package_name: str
    analyzers: dict[str, StateAnalyzerConfig]
