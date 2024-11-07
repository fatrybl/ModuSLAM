"""
Author: Mark Griguletskii
e-mail: mark.griguletskii@skoltech.ru.

Main runner of the SLAM system.
"""

import hydra
import numpy as np

from moduslam.logger.logging_config import setup_logger
from phd.moduslam.main_manager.config import MainManagerConfig
from phd.moduslam.main_manager.manager import MainManager
from phd.moduslam.setup_manager.hydra_config_validator import register_config

np.set_printoptions(precision=6, suppress=True)


@hydra.main(version_base=None, config_name="config", config_path="/configs")
def run(config: MainManagerConfig) -> None:
    """Runs SLAM based on the given configuration."""

    setup_logger(config.logger)

    main_manager = MainManager(config)
    main_manager.build_map()


if __name__ == "__main__":
    register_config()
    run()
