from dataclasses import dataclass


@dataclass
class StateAnalyzerConfig:
    name: str
    module_name: str
    type_name: str
