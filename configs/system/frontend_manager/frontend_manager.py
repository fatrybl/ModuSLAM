from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class FrontendManagerConfig:
    """
    Config for SetupManager.
    """

    params = MISSING
