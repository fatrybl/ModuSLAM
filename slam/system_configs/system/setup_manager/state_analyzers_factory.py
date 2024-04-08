from dataclasses import dataclass

from slam.system_configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


@dataclass
class StateAnalyzerFactoryConfig:
    """Config for HandlerFactory."""

    package_name: str
    analyzers: dict[str, StateAnalyzerConfig]
