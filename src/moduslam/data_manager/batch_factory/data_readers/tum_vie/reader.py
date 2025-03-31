"""This a reader for the TUM dataset."""

import logging
from collections.abc import Iterable, Iterator
from pathlib import Path
from types import TracebackType
from typing import overload

from plum import dispatch

from src.logger.logging_config import data_manager
from src.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from src.moduslam.data_manager.batch_factory.data_readers.data_sources import Source
from src.moduslam.data_manager.batch_factory.data_readers.reader_ABC import DataReader
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.measurement_collector import (
    get_measurement,
    get_next_measurement,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.source import (
    TumVieCsvData,
    TumVieStereoImageData,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.utils import (
    create_sequence,
)
from src.moduslam.data_manager.batch_factory.data_readers.utils import (
    apply_state,
    check_directory,
    check_files,
    filter_table,
    set_state,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.sensors import Sensor
from src.utils.auxiliary_methods import microsec2nanosec
from src.utils.exceptions import (
    DataReaderConfigurationError,
    ItemNotFoundError,
    StateNotSetError,
)

logger = logging.getLogger(data_manager)


class TumVieReader(DataReader):
    _image_file_extension = ".jpg"

    def __init__(self, dataset_params: TumVieConfig):
        """
        Args:
            dataset_params: parameters for TUM VIE dataset.
        """
        dataset_dir = dataset_params.directory

        self._imu = dataset_params.imu_name
        self._stereo = dataset_params.stereo_camera_name
        self._txt_files = dataset_params.txt_files
        self._stereo_data_dirs = dataset_params.stereo_data_dirs

        self._state: dict[str, int] = {
            self._imu: 0,
            self._stereo: 0,
        }

        self._in_context = False
        self._is_configured = False
        self._sensors: dict[str, Sensor] = {}
        self._data_sequence: list[tuple[int, str, int]] = []
        self._data_sequence_iter: Iterator = iter([])

        self._set_root_path(dataset_dir)
        self._check_data_sources(dataset_dir, self._txt_files.values())

        self._sensor_source_table: dict[str, Source] = {
            self._imu: TumVieCsvData(self._txt_files[self._imu]),
            self._stereo: TumVieStereoImageData(
                self._txt_files[self._stereo],
                self._stereo_data_dirs[0],
                self._stereo_data_dirs[1],
                self._image_file_extension,
            ),
        }

    def __enter__(self):
        """Opens all files for reading and initializes iterators."""
        for src in self._sensor_source_table.values():
            src.open()

        apply_state(self._sensor_source_table, self._state)
        self._in_context = True
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
            src.close()

    def configure(self, regime: Stream | TimeLimit, sensors: Iterable[Sensor]) -> None:
        """Configures the reader.

        Args:
            regime: data collection regime.

            sensors: sensors to read data of.

        Raises:
            DataReaderConfigurationError: if no measurements exist for the
            given regime and sensors.
        """
        self._sensors = {sensor.name: sensor for sensor in sensors}
        sensor_names = {sensor.name for sensor in sensors}

        self._data_sequence, indices = create_sequence(self._txt_files, regime, sensor_names)
        self._data_sequence_iter = iter(self._data_sequence)
        for sensor_name, index in indices.items():
            self._state[sensor_name] = index

        used_sensors = set(indices.keys())
        self._sensor_source_table = filter_table(self._sensor_source_table, used_sensors)
        if not self._sensor_source_table:
            msg = "No measurements to read for the defined sensors and the regime."
            logger.critical(msg)
            raise DataReaderConfigurationError(msg)

        self._is_configured = True

    def set_initial_state(self, sensor: Sensor, timestamp: int) -> None:
        """Sets the iterator position for the given sensor and timestamp.

        Args:
            sensor: sensor to set the iterator position.

            timestamp: timestamp to set the iterator position.

        Raises:
            StateNotSetError: if no measurement for the given sensor and timestamp has been found.

        TODO: add tests
        """
        try:
            source = self._sensor_source_table[sensor.name]
        except KeyError:
            msg = f"No source has been found for the sensor {sensor.name}."
            logger.error(msg)
            raise StateNotSetError(msg)

        source.open()

        try:
            set_state(sensor.name, timestamp, self._data_sequence, source)
        except ItemNotFoundError as e:
            logger.error(e)
            raise StateNotSetError(e)

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

        if not self._is_configured:
            msg = "The reader has not been configured. Call the configure() method first."
            logger.critical(msg)
            raise RuntimeError(msg)

        try:
            timestamp, sensor_name, index = next(self._data_sequence_iter)
            self._state[sensor_name] = index
        except StopIteration:
            return None

        sensor = self._sensors[sensor_name]
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

        if not self._is_configured:
            msg = "The reader has not been configured. Call the configure() method first."
            logger.critical(msg)
            raise RuntimeError(msg)

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

    @staticmethod
    def _check_data_sources(dataset_dir: Path, files: Iterable[Path]) -> None:
        """Validate files and subdirectories in dataset directory.

        Args:
            dataset_dir: dataset directory.

        Raises:
            DataReaderConfigurationError:
                1. a data directory does not exist.
                2. txt files have not been found in the dataset directory.
        """
        try:
            check_directory(dataset_dir)
        except NotADirectoryError as e:
            logger.critical(e)
            raise DataReaderConfigurationError(e)

        try:
            check_files(files)

        except FileNotFoundError as e:
            logger.critical(e)
            raise DataReaderConfigurationError(e)

    def _set_root_path(self, root_path: Path) -> None:
        """Sets the root path for all files and directories.

        Args:
            root_path: root path.
        """
        self._txt_files = {sensor: root_path / path for sensor, path in self._txt_files.items()}
        self._stereo_data_dirs = [root_path / path for path in self._stereo_data_dirs]
