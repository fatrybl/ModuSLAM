import logging
from collections.abc import Iterable
from typing import overload

from plum import dispatch
from rosbags.interfaces import Connection
from rosbags.rosbag2 import Reader
from rosbags.typesys import get_typestore

from src.logger.logging_config import data_manager
from src.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from src.moduslam.data_manager.batch_factory.data_readers.locations import (
    Ros2DataLocation,
)
from src.moduslam.data_manager.batch_factory.data_readers.reader_ABC import (
    DataReader,
)
from src.moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2Config,
)
from src.moduslam.data_manager.batch_factory.data_readers.ros2.message_processor import (
    get_msg_processor,
)
from src.moduslam.data_manager.batch_factory.data_readers.ros2.utils.type_alias import (
    RosbagsMessageGenerator,
)
from src.moduslam.data_manager.batch_factory.data_readers.utils import (
    check_directory,
    check_setup,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.sensors import Sensor
from src.utils.exceptions import (
    ConfigurationError,
    DataReaderConfigurationError,
    ItemNotFoundError,
)

logger = logging.getLogger(data_manager)


def get_start_end_time(reader: Reader) -> tuple[int, int]:
    """Gets start and end time of the dataset. The built-in properties
    of rosbags.rosbag2.Reader are not used since it adds extra nanosecond to the end time.

    Args:
        reader: a rosbags ROS-2 reader.

    Returns:
        start and end time of the dataset.
    """
    duration = reader.metadata["duration"]["nanoseconds"]
    start_time = reader.metadata["starting_time"]["nanoseconds_since_epoch"]
    end_time = start_time + duration

    return start_time, end_time


class Ros2Reader(DataReader):
    """ROS2 dataset reader."""

    def __init__(self, dataset_params: Ros2Config):
        """
        Args:
            dataset_params: parameters for ROS-2 dataset.
        """
        self._dataset_directory = dataset_params.directory
        self._sensor_name_topic_table = dataset_params.sensor_topic_mapping

        self._in_context = False
        self._is_configured = False

        self._connections: list[Connection] = []
        self._topic_sensor_table: dict[str, Sensor] = {}
        self._sensor_msg_gen_table: dict[Sensor, RosbagsMessageGenerator] = {}

        try:
            check_directory(self._dataset_directory)
        except NotADirectoryError as e:
            raise DataReaderConfigurationError(e)

        try:
            self._msg_processor = get_msg_processor(dataset_params.ros_distro)
        except NotImplementedError:
            raise DataReaderConfigurationError(
                f"Message processor for {dataset_params.ros_distro} is not implemented."
            )

        self._type_store = get_typestore(dataset_params.ros_distro)

        self._reader = Reader(self._dataset_directory)
        self._all_messages_gen = self._reader.messages()

    def __enter__(self):
        """Opens the dataset for reading."""
        self._reader.open()
        self._in_context = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the dataset."""
        self._reader.close()
        self._in_context = False

    def configure(self, regime: Stream | TimeLimit, sensors: Iterable[Sensor]) -> None:
        """Configures the reader with a regime.

        Args:
            regime: data collection regime.

            sensors: sensors to read data of.

        Raises:
            DataReaderConfigurationError: if no measurements exist for the
            given regime and sensors.
        """
        self._setup_mappings(sensors)

        self._fill_connections()
        if not self._connections:
            logger.critical("No topics to read data from.")
            raise ConfigurationError

        self._all_messages_gen = self._setup_messages_gen(regime, self._reader, self._connections)

        self._setup_sensor_msg_gen_mapping(regime, sensors)

        self._is_configured = True

    def set_initial_state(self, sensor: Sensor, timestamp: float):
        """Sets the iterator position for the sensor at the given timestamp."""

    @overload
    def get_next_element(self) -> Element | None:
        """Gets the next element in the dataset sequentially.

        Returns:
            next element or None.

        Raises:
            RuntimeError: if a method has been called outside the context manager.
        """
        try:
            check_setup(self._in_context, self._is_configured)
        except RuntimeError as e:
            logger.error(e)
            raise

        try:
            connection, timestamp, raw_data = next(self._all_messages_gen)
            msg = self._type_store.deserialize_cdr(raw_data, connection.msgtype)

        except StopIteration:
            return None

        processed_data = self._msg_processor.process(msg, connection.msgtype)

        topic = connection.topic
        sensor = self._topic_sensor_table[topic]

        location = Ros2DataLocation(topic)
        measurement = RawMeasurement(sensor, processed_data)

        return Element(timestamp, measurement, location)

    @overload
    def get_next_element(self, sensor: Sensor) -> Element | None:
        """Gets the next element for a specific sensor.

        Args:
            sensor: a sensor to get the next element for.

        Returns:
            next element or None.

        Raises:
            RuntimeError: if a method has been called outside the context manager.
        """
        try:
            check_setup(self._in_context, self._is_configured)
        except RuntimeError as e:
            logger.error(e)
            raise

        messages_gen = self._sensor_msg_gen_table[sensor]

        try:
            connection, timestamp, raw_data = next(messages_gen)
            msg = self._type_store.deserialize_cdr(raw_data, connection.msgtype)

        except StopIteration:
            return None

        processed_data = self._msg_processor.process(msg, connection.msgtype)

        location = Ros2DataLocation(connection.topic)
        measurement = RawMeasurement(sensor, processed_data)

        return Element(timestamp, measurement, location)

    @dispatch
    def get_next_element(self, element=None):
        """Get an element from the dataset."""

    def get_element(self, element: Element) -> Element:
        """Gets element from a dataset based on the given element w/o raw data.

        Args:
            element: an element w/o raw data.

        Return:
            element with raw data.

        Raises:
            ItemNotFoundError: if no real measurement has been found
            in the dataset for the given element.
        """
        t = element.timestamp
        sensor = element.measurement.sensor
        topic = self._sensor_name_topic_table[sensor.name]
        connections = [с for с in self._connections if с.topic == topic]

        messages_gen = self._reader.messages(connections, t, t + 1)

        try:
            connection, t, raw_data = next(messages_gen)

        except StopIteration:
            error = f"A real measurement has not been found for the given element {element}."
            logger.critical(error)
            raise ItemNotFoundError(error)

        msg = self._type_store.deserialize_cdr(raw_data, connection.msgtype)

        processed_data = self._msg_processor.process(msg, connection.msgtype)

        measurement = RawMeasurement(sensor, processed_data)

        return Element(t, measurement, element.location)

    @staticmethod
    def _setup_messages_gen(
        regime: Stream | TimeLimit, reader: Reader, connections: Iterable[Connection]
    ) -> RosbagsMessageGenerator:
        """Sets up messages generator.

        Args:
            regime: a data reader regime.

            reader: a reader to set up a message generator for.

            connections: connections to set up message generator for.

        Returns:
            messages generator.
        """
        if isinstance(regime, TimeLimit):
            start, stop = int(regime.start), int(regime.stop)
            # add +1 to include the last message
            messages_gen = reader.messages(connections, start, stop + 1)

        else:
            messages_gen = reader.messages(connections)

        return messages_gen

    def _setup_sensor_msg_gen_mapping(
        self, regime: Stream | TimeLimit, sensors: Iterable[Sensor]
    ) -> None:
        """Sets up the generator for each sensor separately.

        Args:
            regime: a data reader regime.

            sensors: sensors to initialize generators for.
        """

        for sensor in sensors:
            topic = self._sensor_name_topic_table[sensor.name]
            connections = [с for с in self._connections if с.topic == topic]

            messages_gen = self._setup_messages_gen(regime, self._reader, connections)

            self._sensor_msg_gen_table[sensor] = messages_gen

    def _setup_mappings(self, sensors: Iterable[Sensor]) -> None:
        """Sets up the mappings.

        Args:
            sensors: sensors to initialize mappings for.
        """
        items = self._sensor_name_topic_table.items()
        names = {sensor.name for sensor in sensors}
        self._sensor_name_topic_table = {name: topic for name, topic in items if name in names}
        self._topic_sensor_table.update(
            {self._sensor_name_topic_table[sensor.name]: sensor for sensor in sensors}
        )

    def _fill_connections(self) -> None:
        """Fills in the connections list."""
        topics = set(self._sensor_name_topic_table.values())
        self._connections = [с for с in self._reader.connections if с.topic in topics]
