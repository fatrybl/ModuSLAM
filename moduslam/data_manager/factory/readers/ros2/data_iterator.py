import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Iterator:
    """Iterator for the sensor`s timestamp file."""

    position: int = 1

    def reset(self):
        self.position = 1

    def next(self):
        self.position += 1

    def get_iter(self):
        return self.position


if __name__ == "__main__":

    folder_path = Path(os.environ["DATA_DIR"])
    bag_path = Path("{}/rosbag2_2023_11_02-12_18_16".format(folder_path))

    my_iterator = Iterator(bag_path)
    my_iterator.sensor_config_setup()
    (sensor, t), iterator = my_iterator.next()
