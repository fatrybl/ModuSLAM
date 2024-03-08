from dataclasses import dataclass


@dataclass
class StateAnalyzerConfig:
    name: str
    module_name: str
    type_name: str


@dataclass
class LidarOdometryStateAnalyzerConfig(StateAnalyzerConfig):
    handler_name: str
