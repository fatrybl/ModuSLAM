from hydra import main

from slam.main_manager.main_manager import MainManager
from configs.main_config import Config

"""
Author: Mark Griguletskii.

Main runner of SLAM system.
"""


@main(config_name='default_config')
def run(cfg: Config):
    """creates Main Manager and runs SLAM
    """
    print(cfg)
    main_manager = MainManager(cfg)
    main_manager.build_map()
    # main_manager.create_batch_with_measurement()
    # main_manager.validate()


if __name__ == "__main__":
    run()
