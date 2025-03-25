"""This a reader for the TUM dataset."""

import logging
from pathlib import Path
from types import TracebackType
from typing import overload

from plum import dispatch

from src.logger.logging_config import data_manager
from src.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from src.moduslam.data_manager.batch_factory.readers.reader_ABC import DataReader
from src.moduslam.data_manager.batch_factory.readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.moduslam.data_manager.batch_factory.readers.tum_vie.measurement_collector import (
    get_measurement,
    get_next_measurement,
)
from src.moduslam.data_manager.batch_factory.readers.tum_vie.source import (
    TumVieCsvData,
    TumVieStereoImageData,
)
from src.moduslam.data_manager.batch_factory.readers.tum_vie.utils import (
    create_sequence,
)
from src.moduslam.data_manager.batch_factory.readers.utils import (
    apply_state,
    check_directory,
    check_files,
    filter_table,
    set_state,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.factory import SensorsFactory
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

    def __init__(self, regime: TimeLimit | Stream, dataset_params: TumVieConfig):
        """
        Args:
            regime: regime to read the data.

            dataset_params: dataset parameters.

        Raises:
            DataReaderConfigurationError: if a date reader is configured improperly:
                1. a data directory does not exist.
                2. csv files have not been found in the dataset directory.
                3. Sensors Factory is empty.
                4. No measurements can be read for the defined regime and sensors.
        """
        super().__init__(regime, dataset_params)

        dataset_dir = dataset_params.directory

        try:
            check_directory(dataset_dir)
        except NotADirectoryError as e:
            logger.critical(e)
            raise DataReaderConfigurationError(e)

        self._imu = dataset_params.imu_name
        self._stereo = dataset_params.stereo_camera_name
        self._csv_files = dataset_params.csv_files
        self._stereo_data_dirs = dataset_params.stereo_data_dirs

        self._set_root_path(dataset_dir)
        try:
            check_files(self._csv_files.values())

        except FileNotFoundError as e:
            logger.critical(e)
            raise DataReaderConfigurationError(e)

        self._state: dict[str, int] = {
            self._imu: 0,
            self._stereo: 0,
        }

        sensor_names = {sensor.name for sensor in SensorsFactory.get_all_sensors()}
        if not sensor_names:
            msg = "No sensors have been defined in the Sensors Factory to read the measurements of."
            logger.critical(msg)
            raise DataReaderConfigurationError(msg)

        self._data_sequence, indices = create_sequence(self._csv_files, regime, sensor_names)
        self._data_sequence_iterator = iter(self._data_sequence)
        for sensor_name, index in indices.items():
            self._state[sensor_name] = index

        base_table = self._base_sensor_source_table()
        used_sensors = set(indices.keys())
        self._sensor_source_table = filter_table(base_table, used_sensors)
        if not self._sensor_source_table:
            msg = "No measurements to read for the defined sensors and the regime."
            logger.critical(msg)
            raise DataReaderConfigurationError(msg)

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
            src.close()

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

        TODO: add exception when get_measurement() fails.
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

    def _base_sensor_source_table(self) -> dict[str, TumVieCsvData | TumVieStereoImageData]:
        """Creates base "sensors <-> source" table."""
        return {
            self._imu: TumVieCsvData(self._csv_files[self._imu]),
            self._stereo: TumVieStereoImageData(
                self._csv_files[self._stereo],
                self._stereo_data_dirs[0],
                self._stereo_data_dirs[1],
                self._image_file_extension,
            ),
        }
