from hydra import main

# from slam.main_manager.main_manager import MainManager
from configs import config as cfg

"""
Author: Mark Griguletskii.

Main runner of SLAM system.
"""


@main(config_name='default_config')
def run(cfg: cfg.Config):
    """creates Main Manager and runs SLAM
    """
    print(cfg)
    # main_manager = MainManager(cfg)
    # main_manager.build_map()


if __name__ == "__main__":
    run()
