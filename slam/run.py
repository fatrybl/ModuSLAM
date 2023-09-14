import sys
import os
sys.path.insert(0, os.getcwd())
from slam.main_manager.main_manager import MainManager
import sys
sys.dont_write_bytecode = True


from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
"""
Author: Mark Griguletskii.

Main runner of SLAM system.
"""


def run():
    # main_manager = MainManager()
    # main_manager.build_map()
    reader = Ros1BagReader()
    while True:
        element = reader.get_element()
        #print(element)
        if(element == None):
            break
if __name__ == "__main__":
    run()
