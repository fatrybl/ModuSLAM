from dataclasses import dataclass, field

from omegaconf import MISSING


@dataclass
class FrontendManagerConfig:
    """
    Config for SetupManager.
    """
    params = MISSING
