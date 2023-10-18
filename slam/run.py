from hydra import main

from slam.main_manager.main_manager import MainManager
from configs.main_config import Config

"""
Author: Mark Griguletskii.

Main runner of SLAM system.
"""


@main(config_name='default_config')
def run(cfg: Config):
    """creates Main Manager and runs SLAM based on configuration
    """
    main_manager = MainManager(cfg)
    main_manager.build_map()


if __name__ == "__main__":
    run()
