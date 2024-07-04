"""
Author: Mark Griguletskii
e-mail: mark.griguletskii@skoltech.ru.

Main runner of the SLAM system.
"""

import hydra
import numpy as np

from moduslam.logger.logging_config import setup_logger
from moduslam.main_manager.main_manager import MainManager
from moduslam.setup_manager.config_validator import register_config
from moduslam.system_configs.main_manager import MainManagerConfig

np.set_printoptions(precision=4, suppress=True)


@hydra.main(version_base=None, config_name="config", config_path="../configs")
def run(config: MainManagerConfig) -> None:
    """Runs SLAM based on the given configuration."""

    # print(OmegaConf.to_yaml(config))

    setup_logger(config.logger)

    main_manager = MainManager(config)
    main_manager.build_map()


if __name__ == "__main__":
    register_config()
    run()
