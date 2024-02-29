"""
Author: Mark Griguletskii
e-mail: mark.griguletskii@skoltech.ru.

Main runner of the SLAM system.
"""

import hydra

from slam.main_manager.main_manager import MainManager
from slam.setup_manager.config_validator import register_config


@hydra.main(version_base=None, config_name="config", config_path="../configs")
def run(cfg) -> None:
    """Creates Main Manager and runs SLAM based on configuration."""

    # print(OmegaConf.to_yaml(cfg))

    main_manager = MainManager(cfg)
    main_manager.build_map()


if __name__ == "__main__":
    register_config()
    run()
