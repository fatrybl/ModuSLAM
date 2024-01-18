from hydra.core.config_store import ConfigStore

from configs.experiments.kaist.config import Config


cs = ConfigStore.instance()
cs.store(name="default_config", node=Config)
