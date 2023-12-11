from dataclasses import dataclass, field
from omegaconf import MISSING


@dataclass
class MapManagerConfig:
    """
    Config for MapManager.
    """
    params = MISSING
