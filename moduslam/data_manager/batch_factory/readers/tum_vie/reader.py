"""This a reader for the TUM dataset."""

import logging
from pathlib import Path
from types import TracebackType
from typing import overload

from plum import dispatch

from moduslam.data_manager.batch_factory.element import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.tum_vie.measurement_collector import (
    get_measurement,
    get_next_measurement,
)
from moduslam.data_manager.batch_factory.readers.tum_vie.source import (
    TumCsvData,
    TumStereoImageData,
)
from moduslam.data_manager.batch_factory.readers.tum_vie.utils import create_sequence
from moduslam.data_manager.batch_factory.readers.utils import (
    apply_state,
    check_directory,
    check_files,
    filter_table,
    set_state,
)
from moduslam.logger.logging_config import data_manager
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from moduslam.utils.auxiliary_methods import microsec2nanosec

logger = logging.getLogger(data_manager)


class TumVieReader(DataReader):

    _image_file_extension = ".jpg"

    def __init__(self, regime: TimeLimit | Stream, dataset_params: TumVieConfig):
        """
        Args:
            regime: regime to read the data.

            dataset_params: dataset parameters.

        Raises:
            FileNotFoundError: if any required file does not exist.

            NotADirectoryError: if the dataset directory does not exist.
        """
        super().__init__(regime, dataset_params)

        dataset_dir = dataset_params.directory
        check_directory(dataset_dir)

        self._imu = dataset_params.imu_name
        self._stereo = dataset_params.stereo_name
        self._csv_files = dataset_params.csv_files
        self._stereo_data_dirs = dataset_params.stereo_data_dirs

        self._set_root_path(dataset_dir)
        check_files(self._csv_files.values())

        self._state: dict[str, int] = {
            self._imu: 0,
            self._stereo: 0,
        }

        sensor_names = {sensor.name for sensor in SensorsFactory.get_all_sensors()}
        self._data_sequence, indices = create_sequence(self._csv_files, regime, sensor_names)
        self._data_sequence_iterator = iter(self._data_sequence)
        for sensor_name, index in indices.items():
            self._state[sensor_name] = index

        base_table = self._base_sensor_source_table()
        used_sensors = set(indices.keys())
        self._sensor_source_table = filter_table(base_table, used_sensors)
        if not self._sensor_source_table:
            logger.warning("No measurements to read for the defined sensors and the regime.")

    def __enter__(self):
        """Opens all files for reading and initializes iterators."""
        self._in_context = True
        for src in self._sensor_source_table.values():
            src.open()
        apply_state(self._sensor_source_table, self._state)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        """Closes all opened files."""
        self._in_context = False
        for src in self._sensor_source_table.values():
            src.flush()

    def set_initial_state(self, sensor: Sensor, timestamp: int) -> None:
        """Sets the iterator position for the given sensor and timestamp.

        Args:
            sensor: sensor to set the iterator position.

            timestamp: timestamp to set the iterator position.

        Raises:
            RuntimeError: if the method is called outside the context manager.

            ItemNotFoundError: if no measurement found for the sensor at the given timestamp.
        """

        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        set_state(sensor.name, timestamp, self._data_sequence, self._sensor_source_table)

    @overload
    def get_next_element(self) -> Element | None:
        """
        @overload.

        Gets element from a dataset sequentially based on iterator position.

        Returns:
            element with raw measurement or None if all measurements from a dataset have already been read.

        Raises:
            RuntimeError: if the method is called outside the context manager.
        """
        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        try:
            timestamp, sensor_name, index = next(self._data_sequence_iterator)
            self._state[sensor_name] = index
        except StopIteration:
            return None

        sensor = SensorsFactory.get_sensor(sensor_name)
        source = self._sensor_source_table[sensor.name]
        message, location = get_next_measurement(source)
        measurement = RawMeasurement(sensor, message.data)
        element = Element(timestamp, measurement, location)
        return element

    @overload
    def get_next_element(self, sensor: Sensor) -> Element | None:
        """
        @overload.

        Gets next element from a dataset for the given sensor.

        Args:
            sensor: sensor to get the measurement of.

        Returns:
            element with raw data or None if all measurements from a dataset have already been read.

        Raises:
            RuntimeError: if the method is called outside the context manager.
        """
        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        try:
            source = self._sensor_source_table[sensor.name]
            message, location = get_next_measurement(source)
        except (StopIteration, KeyError):
            return None

        measurement = RawMeasurement(sensor, message.data)
        timestamp = microsec2nanosec(message.timestamp)
        element = Element(timestamp, measurement, location)
        return element

    @dispatch
    def get_next_element(self, element=None):
        """Get an element from the dataset."""

    def get_element(self, element: Element) -> Element:
        """Gets element from a dataset based on the given element without raw data.

        Args:
            element: element with timestamp.

        Returns:
            element with raw data.

        Raises:
            RuntimeError: if the method is called outside the context manager.
        """
        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        raw_measurement = get_measurement(element.location)
        measurement = RawMeasurement(element.measurement.sensor, raw_measurement)
        element_with_data = Element(element.timestamp, measurement, element.location)
        return element_with_data

    def _set_root_path(self, root_path: Path) -> None:
        """Sets the root path for all files and directories.

        Args:
            root_path: root path.
        """
        self._csv_files = {sensor: root_path / path for sensor, path in self._csv_files.items()}
        self._stereo_data_dirs = [root_path / path for path in self._stereo_data_dirs]

    def _base_sensor_source_table(self) -> dict[str, TumCsvData | TumStereoImageData]:
        """Creates base "sensors <-> source" table."""
        return {
            self._imu: TumCsvData(self._csv_files[self._imu]),
            self._stereo: TumStereoImageData(
                self._csv_files[self._stereo],
                self._stereo_data_dirs[0],
                self._stereo_data_dirs[1],
                self._image_file_extension,
            ),
        }
