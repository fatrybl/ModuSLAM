"""
Author: Mark Griguletskii.

Main runner of SLAM system.
"""
from hydra import main
from hydra.core.config_store import ConfigStore

from configs.experiments.kaist.config import Config
from configs.main_config import MainConfig
from slam.main_manager.main_manager import MainManager

cs = ConfigStore.instance()
cs.store(name="default_config", node=Config)


@main(config_name="default_config")
def run(cfg: MainConfig) -> None:
    """creates Main Manager and runs SLAM based on configuration"""
    main_manager = MainManager(cfg)
    main_manager.build_map()


if __name__ == "__main__":
    run()
