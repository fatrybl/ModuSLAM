from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class BackendManagerConfig:
    """
    Config for SetupManager.
    """

    params = MISSING
