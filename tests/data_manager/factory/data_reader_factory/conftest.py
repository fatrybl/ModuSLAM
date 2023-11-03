from dataclasses import dataclass
from omegaconf import MISSING
import pytest

from hydra.core.config_store import ConfigStore


@dataclass
class Config:
    type: str = MISSING


@pytest.fixture(scope='module', autouse=True)
def register_config():
    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
