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


@hydra.main(version_base=None, config_name="2_lidar", config_path="../configs")  # 1_lidar_imu
def run(config: MainManagerConfig) -> None:
    """Runs SLAM based on the given configuration."""

    print("Testing HYDRA configuration for ModuSLAM for the ROS2 datareader")
    setup_logger(config.logger)
    print("Logger has been set up")
    #
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )

    print("This is the data manager configuration:")
    data_manager_config = config.data_manager

    # for k1, v1 in data_manager_config.items():
    #     print(k1)
    #     for k2, v2 in v1.items():
    #         print("    ", k2)
    #         for k3, v3 in v2.items():
    #             print("        ", k3, ":", v3)

    # print(
    #     "-----------------------------------------------------------------------------------------------------------"
    # )
    #
    # print("This is the setup manager configuration:")
    # setup_manager_config = config.setup_manager
    #
    # for k1, v1 in setup_manager_config.items():
    #     print(k1)
    #     for k2, v2 in v1.items():
    #
    #         if isinstance(v2, str):
    #             print("    ", k2, ":", v2)
    #         else:
    #             for k3, v3 in v2.items():
    #                 if isinstance(v3, str):
    #                     print("        ", k3, ":", v3)
    #                 else:
    #                     for k4, v4 in v3.items():
    #                         print("            ", k4, ":", v4)
    # print(
    #     "-----------------------------------------------------------------------------------------------------------"
    # )
    # print(
    #     "-----------------------------------------------------------------------------------------------------------"
    # )

    print("Initializing the Main Manager")
    main_manager = MainManager(config)
    # print(
    #     f"The {config.data_manager.batch_factory.dataset.name} will initialized with the following parameters:"
    # )
    # print(f"dataset.config:")
    # print(f"    name: {config.data_manager.batch_factory.dataset.name}")
    # print(f"    directory: {config.data_manager.batch_factory.dataset.directory}")
    # print(f"    reader: {config.data_manager.batch_factory.dataset.reader}")
    # print(f"    data stamp: {config.data_manager.batch_factory.dataset.data_stamp_file}")
    #
    # print(f"regime.config: {config.data_manager.batch_factory.regime}")
    # print(f"    name: {config.data_manager.batch_factory.regime.name}")
    # print(f"    start: {config.data_manager.batch_factory.regime.start}")
    # print(f"    stop: {config.data_manager.batch_factory.regime.stop}")
    #
    # print(
    #     "-----------------------------------------------------------------------------------------------------------"
    # )

    print("Starting the build_map method")
    # main_manager.build_map()


if __name__ == "__main__":
    register_config()
    print("Config has been registered.")
    run()
