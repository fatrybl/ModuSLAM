from dataclasses import dataclass


@dataclass
class CandidateFactoryConfig:
    handler_analyzer_table: dict[str, str]
