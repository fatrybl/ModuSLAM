import logging
from typing import overload

from plum import dispatch
from rosbags.rosbag2 import Reader

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.locations import RosbagLocation
from moduslam.data_manager.batch_factory.readers.ros2.utils import read_rosbag
from moduslam.data_manager.batch_factory.readers.utils import check_directory
from moduslam.logger.logging_config import data_manager
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import Ros2Config
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.utils.auxiliary_methods import to_float

logger = logging.getLogger(data_manager)


class Ros2DataReader(DataReader):
    """ROS2 dataset reader."""

    def __init__(self, regime: TimeLimit | Stream, dataset_params: Ros2Config):
        """
        Args:
            regime: Processing regime (stream or time-limited).
            dataset_params: Configuration parameters for the dataset.
        """
        super().__init__(regime, dataset_params)

        logger.debug("Ros2DataReader initialized")  # !!!!!!!!!!!!!!!!!!!!!!!!!!2

        self._dataset_directory = dataset_params.directory
        check_directory(self._dataset_directory)

        self.topics_table = dataset_params.topics_table

        if isinstance(self._regime, TimeLimit):
            if regime.start < 0:
                raise ValueError(f"timestamp start={regime.start} can not be negative")
            if regime.start > regime.stop:
                raise ValueError(f"timestamp start={regime.start} can not be greater than stop={regime.stop}")
            start, stop = to_float(self._regime.start), to_float(self._regime.stop)
            mode = "time_range"
        else:
            start, stop = None, None
            mode = "stream"

        self._sensor_iterator = read_rosbag(
            self._dataset_directory, self.topics_table,
            mode=mode, start_time=start, end_time=stop
        )

        if self._sensor_iterator is None:
            raise ValueError("Error: read_rosbag() returned None!")

    def __enter__(self):
        """Opens the dataset for reading."""
        self._in_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the dataset."""
        self._in_context = False
        logger.info("ROS2 data reader closed.")

    @overload
    def get_next_element(self) -> Element | None:
        """Gets the next element in the dataset sequentially."""
        if not self._in_context:
            logger.critical("Attempted to read data outside of context manager.")
            raise RuntimeError("Reader must be used within a context manager.")

        try:
            index, timestamp, sensor_name, data = next(self._sensor_iterator)
            logger.debug(f"Reading {sensor_name} sensor data at {timestamp}.")
        except (StopIteration, KeyError):
            return None

        sensor = SensorsFactory.get_sensor(sensor_name)
        measurement = RawMeasurement(sensor, data)
        location = RosbagLocation(file=self._dataset_directory, position=index)

        return Element(timestamp=timestamp, measurement=measurement, location=location)

    @overload
    def get_next_element(self, sensor: Sensor):
        """Gets the next element for a specific sensor."""
        pass

    @dispatch
    def get_next_element(self, element=None):
        """Get an element from the dataset."""
        pass

    def set_initial_state(self, sensor: Sensor, timestamp: float):
        """Sets the iterator position for the sensor at the given timestamp.

        Currently not implemented.
        """
        pass

    def get_element(self, element: Element):
        """Gets element from a dataset based on the given element without raw data.

        Currently not implemented.
        """
        pass
