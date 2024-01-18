from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class MapManagerConfig:
    """
    Config for MapManager.
    """

    params = MISSING
