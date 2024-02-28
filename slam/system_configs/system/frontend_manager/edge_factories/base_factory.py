from dataclasses import dataclass


@dataclass
class EdgeFactoryConfig:
    """Base class for edge factory config."""

    name: str
    class_name: str
