"""ROS2 dataset Reader"""

import logging
import os
from pathlib import Path
from typing import overload

from plum import dispatch
from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.ros2.utils import (
    get_rosbag_sensors,
    get_connections,
    map_sensors,
)
from moduslam.data_manager.batch_factory.readers.utils import (
    check_directory,
)
from moduslam.logger.logging_config import data_manager
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.utils.auxiliary_dataclasses import TimeRange

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

        self._in_context = False

        check_directory(self._dataset_directory)
        self.sensors_table = dataset_params.sensors_table
        # For testing purposes
        self.sensors_table = {
            "stereo_camera_left": "left",
            "imu": "xsens",
        }

        # TODO: Change print statements with Logger functions
        logger.info("ROS2 data reader created.")
        logger.debug(f"Dataset directory: {self._dataset_directory}")
        print("\nInitial sensors table:")
        print(self.sensors_table)

        self.sensors = get_rosbag_sensors(self._dataset_directory)
        print("\nSensors from rosbag:")
        print(self.sensors)

        self.connection_list, self.sensors = map_sensors(self.sensors_table, self.sensors)
        print("\nMapped sensors:")
        print(self.sensors)

        self.connections = get_connections(self.connection_list, self._dataset_directory)
        print("\nConnections from rosbag:")
        print(self.connections)

        if isinstance(self._regime, TimeLimit):
            self._time_range = TimeRange(self._regime.start, self._regime.stop)

    def __enter__(self):
        """Opens the dataset for reading."""
        print("Opening the Rosbag now")
        self._in_context = True
        self.reader = Reader(self._dataset_directory)
        self.reader.open()
        self.rosbag_iter = self.rosbag_iterator()
        return self.reader

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the dataset."""
        self._in_context = False
        if self.reader:
            self.reader.close()
            self.reader = None

    def set_initial_state(self, sensor: Sensor, timestamp: int):
        """Sets the iterator position for the sensor at the given timestamp.

        Args:
            sensor: sensor to set the iterator position.

            timestamp: timestamp to set the iterator position.

        Raises:
            ItemNotFoundError: if no measurement found for the sensor at the given timestamp.
        """
        pass

    def rosbag_iterator(self):
        """Generator for Rosbag data

        Yields:
            tuple: timestamp, sensor_name, message


        """
        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        for i, (connection, timestamp, rawdata) in enumerate(
            self.reader.messages(connections=self.connections)
        ):
            sensor_name = "no sensor"
            sensor_id = connection.id
            sensor = connection.topic.split("/")[1]
            data_type = connection.msgtype.split("/")[-1]
            msg = deserialize_cdr(rawdata, connection.msgtype)

            for single_sensor in self.sensors:
                if single_sensor["sensor"] == sensor:
                    sensor_name = single_sensor["sensor_name"]
                    break

            yield (i, timestamp, sensor_name, msg)

    @overload
    def get_next_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """
        # TODO: use yield to return elements from the rosbags one by one.

        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        try:
            index, timestamp, sensor_name, data = next(self.rosbag_iter)
            print("Sucessfully obtained sensor data")

        except (StopIteration, KeyError):
            return None

        sensor = SensorsFactory.get_sensor(sensor_name)
        measurement = RawMeasurement(sensor, data)
        # timestamp = to_int(timestamp)

        element = Element(timestamp, measurement, index)

        return None

    @overload
    def get_next_element(self, sensor: Sensor):
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Args:
            sensor: sensor to get the element for

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """

        pass

    @dispatch
    def get_next_element(self, element=None):
        """Get an element from the dataset."""

    def get_element(self):
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """

        pass


if __name__ == "__main__":

    print("Testing ROS2 data reader")
    folder_path = Path(os.environ["DATA_DIR"])
    print(folder_path)
    bag_path = Path("{}/rosbag2_2024_1713944720".format(folder_path))

    timelimit1 = TimeLimit(start=10, stop=20)
    timelimit2 = Stream()
    ros2_config = Ros2Config(directory=bag_path)

    reader = Ros2DataReader(regime=timelimit1, dataset_params=ros2_config)

    with reader as r:
        print("Rosbag opened successfully")
        user_input = input("Get sensor read? (y/n): ")

        while user_input == "y":
            element = reader.get_next_element()
            print(element)
            user_input = input("Get another sensor read? (y/n): ").lower()
