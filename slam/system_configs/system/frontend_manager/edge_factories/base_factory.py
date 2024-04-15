from dataclasses import dataclass, field


@dataclass
class EdgeFactoryConfig:
    """Base edge factory config."""

    name: str
    type_name: str
    module_name: str
    noise_model: str
    search_time_margin: int = field(default=0, metadata={"help": "Time margin in nanoseconds."})
