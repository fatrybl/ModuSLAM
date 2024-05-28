from dataclasses import dataclass


@dataclass
class CandidateFactoryConfig:
    """Base candidate factory configuration."""

    handler_state_analyzer_table: dict[str, str]
