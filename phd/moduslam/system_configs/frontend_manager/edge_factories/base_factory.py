from dataclasses import dataclass, field


@dataclass
class EdgeFactoryConfig:
    """Base edge factory configuration."""

    name: str
    type_name: str
    module_name: str
    search_time_margin: float = field(
        default=0.0, metadata={"help": "Time margin in seconds for the graph vertices search."}
    )
