"""ROS2 dataset Reader"""

import logging
import os
from pathlib import Path

from rosbags.rosbag2 import Reader

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.utils import (
    check_directory,
)
from moduslam.data_manager.factory.readers.ros2.rosbags2_manager import Rosbags2Manager  # UPDATE
# from moduslam.data_manager.factory.readers.ros2.data_iterator import Iterator
from moduslam.logger.logging_config import data_manager
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(data_manager)


class Ros2DataReader(DataReader):
    """Data reader for ROS2 in test."""

    def __init__(self, regime: TimeLimit | Stream, dataset_params: Ros2Config):
        """
        Args:
            regime: regime to read the data.

            dataset_params: dataset parameters.

        Raises:
            FileNotFoundError: if any required file does not exist.

            NotADirectoryError: if the dataset directory does not exist.
        """
        self._dataset_directory: Path = dataset_params.directory
        self._regime = regime

        check_directory(self._dataset_directory)
        self.sensors_table = dataset_params.sensors_table
        print("\nInitial sensors table:")
        print(self.sensors_table)

        self.reader = None
        print(f"Reader: {self.reader}")

        if isinstance(self._regime, TimeLimit):
            self._time_range = TimeRange(self._regime.start, self._regime.stop)
            self.rosbags_manager = Rosbags2Manager(
                self._dataset_directory, self.sensors_table, self._time_range
            )

        else:
            self.rosbags_manager = Rosbags2Manager(self._dataset_directory, self.sensors_table)

    def __enter__(self):
        """Opens the dataset for reading."""
        self.reader = Reader(self._dataset_directory)
        self.reader.open()
        return self.reader

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the dataset."""
        if self.reader:
            self.reader.close()
            self.reader = None

    def set_initial_state(self, sensor: Sensor, timestamp: int) -> None:
        """
        @overload.
        Sets the iterator(s) position(s) for the given sensor and timestamp.

        Args:
            sensor: sensor to set the iterator(s) position(s) to.

            timestamp: timestamp to set the iterator(s) position(s) to.

        Raises:
            RuntimeError: if the method is called outside the context manager.

            ItemNotFoundError: if no measurement for the given sensor and timestamp is found.
        """
        pass

    def get_next_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """
        # TODO: use yield to return elements from the rosbags one by one.
        pass

    def get_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """

        sensor_id, location, message, t = self.rosbags_manager.next_sensor_read()
        print(f"Got sensor: {sensor_id}")
        for sensor in self.rosbags_manager.sensors_list:
            if sensor["id"] == sensor_id:
                sensor_name = sensor["sensor_name"]
                print(f"That means sensor {sensor_name}")
                break
        try:
            sensor = SensorsFactory.get_sensor(sensor_name)
            # TODO Check that sensor_name MATCHES with the name in the sensors configs

        # except StopIteration:
        except ItemNotFoundError as e:
            print(f"Failed to get sensor {sensor_name} with error message: {e}")
            return None

        # timestamp: int = as_int(t)
        if isinstance(self._regime, TimeLimit) and t > self._time_range.stop:
            return None

        measurement = RawMeasurement(sensor, message)
        element = Element(t, measurement, location)

        return element


if __name__ == "__main__":

    print("Testing ROS2 data reader")
    folder_path = Path(os.environ["DATA_DIR"])
    print(folder_path)
    bag_path = Path("{}/rosbag2_2024_1713944720".format(folder_path))

    timelimit1 = TimeLimit(start=10, stop=20)
    timelimit2 = Stream()
    ros2_config = Ros2Config(directory=bag_path)

    reader = Ros2DataReader(regime=timelimit1, dataset_params=ros2_config)

    my_config = SensorFactoryConfig()
    SensorsFactory.init_sensors(config=my_config)

    reader.get_element()
