from dataclasses import dataclass, field

from omegaconf import MISSING


@dataclass
class BackendManagerConfig:
    """
    Config for SetupManager.
    """
    params = MISSING
