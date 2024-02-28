from hydra.core.config_store import ConfigStore

from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig
from configs.system.data_manager.batch_factory.regime import StreamConfig
from configs.system.main_manager import MainManagerConfig


def register_config():
    cs = ConfigStore.instance()
    cs.store(name="structured_schema_config", node=MainManagerConfig)
    cs.store(group="datasets", name="base_kaist_dataset", node=KaistConfig)
    cs.store(group="regimes", name="base_time_limit", node=StreamConfig)
