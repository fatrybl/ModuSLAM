import os
from dataclasses import dataclass
from pathlib import Path

from slam.data_manager.factory.readers.ros2_reader.get_data import DataGrabber


@dataclass
class Iterator:
    """Iterator for the sensor`s timestamp file."""

    bagpath:Path
    msg_limit:int = 10000
    position: int = 0
    data: list = None


    def reset(self):
        self.position = 0
        self._get_data(self.position)


    def _get_data(self, pos:int):
        return DataGrabber.iter_rosbag(self.bagpath, pos, self.msg_limit)


    def next(self):
            self.position += 1
            return self._get_data(self.position)



if __name__ == "__main__":

    folder_path = Path(os.environ["DATA_DIR"])
    bag_path = Path("{}/rosbag2_2023_11_02-12_18_16".format(folder_path))
    my_iterator = Iterator(bag_path)
    for i in range(20):
        print(my_iterator.next())

        if i == 10:
            my_iterator.reset()
            print("Resetting the iterator")
