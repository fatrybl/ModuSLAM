from dataclasses import dataclass


@dataclass
class EdgeFactoryConfig:
    """Base edge factory config."""

    name: str
    type_name: str
    module_name: str
    noise_model: str
