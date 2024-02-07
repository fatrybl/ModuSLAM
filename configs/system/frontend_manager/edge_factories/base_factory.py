from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class EdgeFactoryConfig:
    """
    Base class for edge factory config.
    """

    name: str = MISSING
    class_name: str = MISSING
