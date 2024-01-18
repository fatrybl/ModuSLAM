from dataclasses import dataclass

import pytest
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING


@dataclass
class Config:
    type: str = MISSING


@pytest.fixture(scope="module", autouse=True)
def register_config():
    cs = ConfigStore.instance()
    cs.store(name="config", node=Config)
