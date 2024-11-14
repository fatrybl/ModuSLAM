"""Kaist Urban Dataset reader."""

import logging
from pathlib import Path
from types import TracebackType
from typing import overload

from plum import dispatch

from moduslam.utils.auxiliary_methods import to_int
from phd.logger.logging_config import data_manager
from phd.moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from phd.moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from phd.moduslam.data_manager.batch_factory.readers.data_sources import (
    CsvData,
    PointcloudData,
    StereoImageData,
)
from phd.moduslam.data_manager.batch_factory.readers.kaist.config_objects.base import (
    KaistConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.kaist.measurement_collector import (
    get_measurement,
    get_next_measurement,
)
from phd.moduslam.data_manager.batch_factory.readers.kaist.utils import create_sequence
from phd.moduslam.data_manager.batch_factory.readers.utils import (
    apply_state,
    check_directory,
    check_files,
    filter_table,
    set_state,
)
from phd.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from phd.moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from phd.moduslam.setup_manager.sensors_factory.sensors import Sensor

logger = logging.getLogger(data_manager)


class KaistReader(DataReader):

    _image_extension = ".png"
    _pointcloud_extension = ".bin"

    def __init__(self, regime: TimeLimit | Stream, dataset_params: KaistConfig):
        """
        Args:
            regime: regime to read the data.

            dataset_params: dataset parameters.

        Raises:
            FileNotFoundError: if any required file does not exist.

            NotADirectoryError: if the dataset directory does not exist.
        """
        super().__init__(regime, dataset_params)

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

        dataset_dir = dataset_params.directory
        check_directory(dataset_dir)
        self._set_root_path(dataset_dir)
        check_files((*self._csv_files.values(), self._timestamp_file))

        self._state: dict[str, int] = {
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

        sensor_names = {sensor.name for sensor in SensorsFactory.get_all_sensors()}
        self._data_sequence, indices = create_sequence(self._timestamp_file, regime, sensor_names)
        self._data_sequence_iterator = iter(self._data_sequence)
        for sensor_name, index in indices.items():
            self._state[sensor_name] = index

        base_table = self._base_sensor_source_table()
        used_sensors = set(indices.keys())
        self._sensor_source_table = filter_table(base_table, used_sensors)
        if not self._sensor_source_table:
            logger.error("No measurements to read for the defined sensors and the regime.")

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
        msg_timestamp = to_int(message.timestamp)
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

        try:
            source = self._sensor_source_table[sensor.name]
            message, location = get_next_measurement(source)
        except (StopIteration, KeyError):
            return None

        measurement = RawMeasurement(sensor, message.data)
        timestamp = to_int(message.timestamp)
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
        """
        if not self._in_context:
            logger.critical(self._context_error_msg)
            raise RuntimeError(self._context_error_msg)

        raw_measurement = get_measurement(element.location)
        measurement = RawMeasurement(element.measurement.sensor, raw_measurement.data)
        element_with_data = Element(element.timestamp, measurement, element.location)
        return element_with_data

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

    def _base_sensor_source_table(self) -> dict[str, CsvData | PointcloudData | StereoImageData]:
        """Base "sensors <-> source" table of Kaist Urban datasets."""
        ext = self._pointcloud_extension
        return {
            self._imu: CsvData(self._csv_files[self._imu]),
            self._fog: CsvData(self._csv_files[self._fog]),
            self._gps: CsvData(self._csv_files[self._gps]),
            self._vrs_gps: CsvData(self._csv_files[self._vrs_gps]),
            self._altimeter: CsvData(self._csv_files[self._altimeter]),
            self._encoder: CsvData(self._csv_files[self._encoder]),
            self._lidar2D_back: PointcloudData(self._lidar_data_dirs[self._lidar2D_back], ext),
            self._lidar2D_middle: PointcloudData(self._lidar_data_dirs[self._lidar2D_middle], ext),
            self._lidar3D_left: PointcloudData(self._lidar_data_dirs[self._lidar3D_left], ext),
            self._lidar3D_right: PointcloudData(self._lidar_data_dirs[self._lidar3D_right], ext),
            self._stereo: StereoImageData(
                self._stereo_data_dirs[0], self._stereo_data_dirs[1], self._image_extension
            ),
        }
