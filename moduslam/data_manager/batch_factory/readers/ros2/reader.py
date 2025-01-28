"""ROS2 dataset Reader."""

import logging
from typing import overload

from plum import dispatch
from rosbags.rosbag2 import Reader

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.locations import RosbagLocation
from moduslam.data_manager.batch_factory.readers.ros2.utils import (
    check_setup_sensors,
    get_rosbag_sensors,
    rosbag_iterator,
)
from moduslam.data_manager.batch_factory.readers.utils import check_directory
from moduslam.logger.logging_config import data_manager
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_methods import to_float

logger = logging.getLogger(data_manager)

SensorsFactory.get_all_sensors()


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

        super().__init__(regime, dataset_params)

        self._dataset_directory = dataset_params.directory
        check_directory(self._dataset_directory)

        self._sensors_in_config = dataset_params.sensors_table
        self.topics_table = dataset_params.topics_table

        self._sensors_in_factory = SensorsFactory.get_all_sensors()
        self._sensors_table = check_setup_sensors(self._sensors_in_config, self._sensors_in_factory)

        self._sensors = get_rosbag_sensors(
            self._dataset_directory, self._sensors_table, self.topics_table
        )

        self._rosbag_reader = Reader(self._dataset_directory)

        self._connections = []

        if isinstance(self._regime, TimeLimit):

            start, stop = to_float(self._regime.start), to_float(self._regime.stop)
            self._time_range = TimeRange(start, stop)
            self._rosbag_iterator = rosbag_iterator(
                self._rosbag_reader,
                self._sensors,
                self._connections,
                self._time_range,
            )
        else:
            self._rosbag_iterator = rosbag_iterator(
                self._rosbag_reader,
                self._sensors,
                self._connections,
            )

    def __enter__(self):
        """Opens the dataset for reading."""
        self._in_context = True
        self._rosbag_reader.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the dataset."""
        self._in_context = False
        self._rosbag_reader.close()
        logger.info("ROS2 data reader closed.")

    def set_initial_state(self, sensor: Sensor, timestamp: float):
        """Sets the iterator position for the sensor at the given timestamp.

        Args:
            sensor: sensor to set the iterator position.

            timestamp: timestamp to set the iterator position.

        Raises:
            ItemNotFoundError: if no measurement found for the sensor at the given timestamp.
        """
        pass

    @overload
    def get_next_element(self):
        """@overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """

        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        try:
            index, timestamp, sensor_name, data = next(self._rosbag_iterator)
            logger.debug(f"Reading {sensor_name} sensor data at {timestamp}.")

        except (StopIteration, KeyError):
            return None

        sensor = SensorsFactory.get_sensor(sensor_name)
        measurement = RawMeasurement(sensor, data)
        location = RosbagLocation(file=self._dataset_directory, position=index)
        # timestamp = to_int(timestamp)

        element = Element(timestamp=timestamp, measurement=measurement, location=location)

        return element

    @overload
    def get_next_element(self, sensor: Sensor):
        """@overload.
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

    def get_element(self, element: Element):
        """Gets element from a dataset based on the given element without raw data.

        Args:
            element: element with timestamp.

        Returns:
            element with raw data.

        Raises:
            RuntimeError: if the method is called outside the context manager.
        """

        pass
