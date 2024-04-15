from dataclasses import dataclass


@dataclass
class CandidateFactoryConfig:
    handler_state_analyzer_table: dict[str, str]
