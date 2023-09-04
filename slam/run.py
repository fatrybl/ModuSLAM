import sys
import os
sys.path.insert(0, os.getcwd())
from slam.main_manager.main_manager import MainManager
import sys
sys.dont_write_bytecode = True


"""
Author: Mark Griguletskii.

Main runner of SLAM system.
"""


def run():
    main_manager = MainManager()
    main_manager.build_map()


if __name__ == "__main__":
    run()
