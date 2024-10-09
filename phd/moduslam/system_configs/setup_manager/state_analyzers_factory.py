from dataclasses import dataclass

from moduslam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


@dataclass
class StateAnalyzersFactoryConfig:
    """State analyzer factory configuration."""

    package_name: str
    analyzers: dict[str, StateAnalyzerConfig]
