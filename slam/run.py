"""
Author: Mark Griguletskii
e-mail: mark.griguletskii@skoltech.ru.

Main runner of the SLAM system.
"""

import hydra
from omegaconf import OmegaConf

from slam.logger.logging_config import setup_logger
from slam.main_manager.main_manager import MainManager
from slam.setup_manager.config_validator import register_config
from slam.system_configs.main_manager import MainManagerConfig


@hydra.main(version_base=None, config_name="lidar", config_path="../configs")
def run(config: MainManagerConfig) -> None:
    """Runs SLAM based on the given configuration."""
    print(OmegaConf.to_yaml(config.setup_manager))

    setup_logger(config.logger)

    main_manager = MainManager(config)
    main_manager.build_map()


if __name__ == "__main__":
    register_config()
    run()
