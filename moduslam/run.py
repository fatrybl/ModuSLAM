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


@hydra.main(version_base=None, config_name="1_lidar_imu", config_path="../configs")
def run(config: MainManagerConfig) -> None:
    """Runs SLAM based on the given configuration."""

    print("Testing HYDRA configuration for ModuSLAM for the ROS2 datareader")
    setup_logger(config.logger)
    print("Logger has been set up. This is the data manager configuration: ")
    print(config.data_manager)
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("Initializing the Main Manager")
    main_manager = MainManager(config)
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    main_manager.build_map()


if __name__ == "__main__":
    print("Running the SLAM system")
    register_config()
    print("Config has been registered.")
    run()
