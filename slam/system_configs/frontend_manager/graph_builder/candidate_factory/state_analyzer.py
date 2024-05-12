from dataclasses import dataclass, field


@dataclass
class StateAnalyzerConfig:
    """Base state analyzer configuration."""

    name: str
    module_name: str
    type_name: str
    handlers_names: list[str] = field(
        metadata={"info": "names of handlers to be used by the analyzer"}
    )
