from dataclasses import dataclass
from hydra.core.config_store import ConfigStore

#from configs.experiments.kaist.config import Config as Cfg
# from configs.experiments.kaist_test.config import Config
from configs.experiments.ros1.config import ConfigRos1, Ros1DM


@dataclass
class Config(ConfigRos1):
    pass

# from configs.experiments.kaist.config import Config



cs = ConfigStore.instance()
cs.store(name='default_config', node=ConfigRos1)
