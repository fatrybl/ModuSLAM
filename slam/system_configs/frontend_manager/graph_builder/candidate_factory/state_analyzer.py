from dataclasses import dataclass


@dataclass
class StateAnalyzerConfig:
    """Base state analyzer configuration."""

    name: str
    module_name: str
    type_name: str
    handler_name: str
