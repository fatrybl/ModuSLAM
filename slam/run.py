"""
Author: Mark Griguletskii
e-mail: mark.griguletskii@skoltech.ru.

Main runner of the SLAM system.
"""

import hydra
import numpy as np

from slam.logger.logging_config import setup_logger
from slam.main_manager.main_manager import MainManager
from slam.setup_manager.config_validator import register_config
from slam.system_configs.main_manager import MainManagerConfig

np.set_printoptions(precision=4, suppress=True)


@hydra.main(version_base=None, config_name="1_lidar_imu", config_path="../configs")
def run(config: MainManagerConfig) -> None:
    """Runs SLAM based on the given configuration."""

    setup_logger(config.logger)

    main_manager = MainManager(config)
    main_manager.build_map()


if __name__ == "__main__":
    register_config()
    run()
