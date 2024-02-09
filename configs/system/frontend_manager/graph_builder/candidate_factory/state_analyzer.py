from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class StateAnalyzerConfig:
    name: str = MISSING
    module_name: str = MISSING
    type_name: str = MISSING
