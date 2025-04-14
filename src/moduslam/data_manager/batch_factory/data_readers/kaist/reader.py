"""Kaist Urban Dataset reader."""

import logging
from collections.abc import Iterable, Iterator
from pathlib import Path
from types import TracebackType
from typing import overload

from plum import dispatch

from src.logger.logging_config import data_manager
from src.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from src.moduslam.data_manager.batch_factory.data_readers.data_sources import (
    CsvData,
    PointCloudData,
    Source,
    StereoImageData,
)
from src.moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.kaist.measurement_collector import (
    get_measurement,
    get_next_measurement,
)
from src.moduslam.data_manager.batch_factory.data_readers.kaist.utils import (
    create_sequence,
)
from src.moduslam.data_manager.batch_factory.data_readers.reader_ABC import DataReader
from src.moduslam.data_manager.batch_factory.data_readers.utils import (
    apply_state,
    check_directory,
    check_files,
    filter_table,
    set_state,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.sensors import Sensor
from src.utils.auxiliary_methods import str_to_int
from src.utils.exceptions import (
    DataReaderConfigurationError,
    ItemNotFoundError,
    StateNotSetError,
)

logger = logging.getLogger(data_manager)


class KaistReader(DataReader):
    _image_extension = ".png"
    _pointcloud_extension = ".bin"

    def __init__(self, dataset_params: KaistConfig):
        """
        Args:
            dataset_params: Kaist Urban dataset parameters.
        """
        self._imu = dataset_params.imu_name
        self._fog = dataset_params.fog_name
        self._gps = dataset_params.gps_name
        self._vrs_gps = dataset_params.vrs_gps_name
        self._altimeter = dataset_params.altimeter_name
        self._encoder = dataset_params.encoder_name
        self._lidar2D_back = dataset_params.lidar_2D_back_name
        self._lidar2D_middle = dataset_params.lidar_2D_middle_name
        self._lidar3D_left = dataset_params.lidar_3D_left_name
        self._lidar3D_right = dataset_params.lidar_3D_right_name
        self._stereo = dataset_params.stereo_name

        self._timestamp_file = dataset_params.data_stamp_file
        self._csv_files = dataset_params.csv_files
        self._lidar_data_dirs = dataset_params.lidar_data_dirs
        self._stereo_data_dirs = dataset_params.stereo_data_dirs

        self._state = {
            self._imu: 0,
            self._fog: 0,
            self._gps: 0,
            self._vrs_gps: 0,
            self._altimeter: 0,
            self._encoder: 0,
            self._lidar2D_back: 0,
            self._lidar2D_middle: 0,
            self._lidar3D_left: 0,
            self._lidar3D_right: 0,
            self._stereo: 0,
        }
        self._in_context = False
        self._is_configured = False
        self._time_limit_end: int = 0
        self._data_sequence: list[tuple[int, str, int]] = []
        self._data_sequence_iter: Iterator = iter([])
        self._sensors: dict[str, Sensor] = {}

        self._set_root_path(dataset_params.directory)
        self._check_data_sources(dataset_params.directory)

        ext = self._pointcloud_extension
        self._sensor_source_table: dict[str, Source] = {
            self._imu: CsvData(self._csv_files[self._imu]),
            self._fog: CsvData(self._csv_files[self._fog]),
            self._gps: CsvData(self._csv_files[self._gps]),
            self._vrs_gps: CsvData(self._csv_files[self._vrs_gps]),
            self._altimeter: CsvData(self._csv_files[self._altimeter]),
            self._encoder: CsvData(self._csv_files[self._encoder]),
            self._lidar2D_back: PointCloudData(self._lidar_data_dirs[self._lidar2D_back], ext),
            self._lidar2D_middle: PointCloudData(self._lidar_data_dirs[self._lidar2D_middle], ext),
            self._lidar3D_left: PointCloudData(self._lidar_data_dirs[self._lidar3D_left], ext),
            self._lidar3D_right: PointCloudData(self._lidar_data_dirs[self._lidar3D_right], ext),
            self._stereo: StereoImageData(
                self._stereo_data_dirs[0], self._stereo_data_dirs[1], self._image_extension
            ),
        }

    def __enter__(self):
        """Opens all files for reading and initializes iterators with the latest
        state."""
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

        self._data_sequence, indices = create_sequence(self._timestamp_file, regime, sensor_names)
        self._data_sequence_iter = iter(self._data_sequence)

        if isinstance(regime, Stream):
            self._time_limit_end = self._data_sequence[-1][0]

        else:
            self._time_limit_end = int(regime.stop)

        for sensor_name, index in indices.items():
            self._state[sensor_name] = index

        used_sensors = set(indices.keys())
        self._sensor_source_table = filter_table(self._sensor_source_table, used_sensors)

        if not self._sensor_source_table:
            msg = "No measurements to read for the defined sensors and the regime."
            logger.critical(msg)
            raise DataReaderConfigurationError

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
        msg_timestamp = str_to_int(message.timestamp)
        if timestamp != msg_timestamp:
            msg = (
                f"There is no real measurement for the sensor {sensor_name} at the timestamp {timestamp}."
                f"Check the data source."
            )
            logger.critical(msg)
            raise ValueError(msg)
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

        timestamp = str_to_int(message.timestamp)

        if timestamp > self._time_limit_end:
            return None

        measurement = RawMeasurement(sensor, message.data)
        element = Element(timestamp, measurement, location)
        return element

    @dispatch
    def get_next_element(self, element=None):
        """Gets an element from the dataset."""

    def get_element(self, element: Element) -> Element:
        """Gets element from a dataset based on the given element without raw data.

        Args:
            element: element with timestamp.

        Returns:
            element with raw data.

        Raises:
            RuntimeError: if the method is called outside the context manager.

        TODO: add try block to catch exceptions from get_measurement()
        """
        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        raw_measurement = get_measurement(element.location)
        measurement = RawMeasurement(element.measurement.sensor, raw_measurement.data)
        element_with_data = Element(element.timestamp, measurement, element.location)
        return element_with_data

    def _check_data_sources(self, dataset_dir: Path) -> None:
        """Validate files and subdirectories in dataset directory.

        Args:
            dataset_dir: dataset directory.

        Raises:
            DataReaderConfigurationError:
                1. a data directory does not exist.
                2. csv files have not been found in the dataset directory.
        """
        try:
            check_directory(dataset_dir)
        except NotADirectoryError as e:
            logger.critical(e)
            raise DataReaderConfigurationError(e)

        csv_files = (*self._csv_files.values(), self._timestamp_file)
        try:
            check_files(csv_files)

        except FileNotFoundError as e:
            logger.critical(e)
            raise DataReaderConfigurationError(e)

    def _set_root_path(self, root_path: Path) -> None:
        """Sets the root path for all files and directories.

        Args:
            root_path: root path.
        """
        self._csv_files = {sensor: root_path / path for sensor, path in self._csv_files.items()}
        self._lidar_data_dirs = {
            sensor: root_path / path for sensor, path in self._lidar_data_dirs.items()
        }
        self._stereo_data_dirs = [root_path / path for path in self._stereo_data_dirs]
        self._timestamp_file = root_path / self._timestamp_file
