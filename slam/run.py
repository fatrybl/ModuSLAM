
import sys
sys.dont_write_bytecode = True
from hydra import main

from slam.main_manager.main_manager import MainManager
from configs.main_config import Config

from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
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
    # main_manager.create_batch_with_requests()
    # main_manager.create_batch_with_measurement()
    # main_manager.validate()


if __name__ == "__main__":
    run()
