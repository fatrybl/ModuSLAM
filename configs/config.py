from dataclasses import dataclass

from hydra.core.config_store import ConfigStore

from configs.experiments.kaist.config import Kaist
from configs.experiments.kaist_test.config import TestKaist
from configs.experiments.ros1.config import Ros1


@dataclass
class Config(Ros1):
    pass


cs = ConfigStore.instance()
cs.store(name='default_config', node=Config)
