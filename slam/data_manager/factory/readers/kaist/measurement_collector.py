import logging
from pathlib import Path
from typing import Callable, overload

import numpy as np
import numpy.typing as npt
from PIL import Image
from plum import dispatch

from slam.data_manager.factory.element import Location
from slam.data_manager.factory.readers.kaist.auxiliary_classes import (
    BinaryDataLocation,
    CsvDataLocation,
    Message,
    StereoImgDataLocation,
)
from slam.data_manager.factory.readers.kaist.iterators import FileIterator
from slam.utils.auxiliary_methods import as_int
from slam.utils.exceptions import ExternalModuleException, ItemNotFoundError

logger = logging.getLogger(__name__)


class MeasurementCollector:
    """Collects sensors` measurements from Kaist Urban Dataset."""

    _INCORRECT_TIMESTAMP: int = -111111111
    _IMAGE_EXTENSION: str = ".png"
    _BINARY_EXTENSION: str = ".bin"

    imu: str = "imu"
    fog: str = "fog"
    altimeter: str = "altimeter"
    gps: str = "gps"
    vrs: str = "vrs"
    encoder: str = "encoder"
    sick_back: str = "sick_back"
    sick_middle: str = "sick_middle"
    velodyne_left: str = "velodyne_left"
    velodyne_right: str = "velodyne_right"
    stereo: str = "stereo"

    def __init__(
        self,
        lidar_data_dirs_table: dict[str, Path],
        stereo_data_dirs_table: dict[str, Path],
    ):

        self._lidars_table = lidar_data_dirs_table
        self._stereo_left_data_dir = list(stereo_data_dirs_table.values())[0]
        self._stereo_right_data_dir = list(stereo_data_dirs_table.values())[1]

        self._sensors_data_getters: dict[str, Callable] = {
            self.imu: self._get_imu_data,
            self.fog: self._get_fog_data,
            self.altimeter: self._get_altimeter_data,
            self.gps: self._get_gps_data,
            self.vrs: self._get_vrs_gps_data,
            self.encoder: self._get_encoder_data,
            self.sick_back: self._get_sick_back_data,
            self.sick_middle: self._get_sick_middle_data,
            self.velodyne_left: self._get_velodyne_left_data,
            self.velodyne_right: self._get_velodyne_right_data,
            self.stereo: self._get_stereo_data,
        }

    def _get_imu_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, CsvDataLocation]:
        if timestamp is None:
            return self._get_csv_data(iterator)
        else:
            return self._get_csv_data(iterator, timestamp)

    def _get_fog_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, CsvDataLocation]:
        if timestamp is None:
            return self._get_csv_data(iterator)
        else:
            return self._get_csv_data(iterator, timestamp)

    def _get_encoder_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, CsvDataLocation]:
        if timestamp is None:
            return self._get_csv_data(iterator)
        else:
            return self._get_csv_data(iterator, timestamp)

    def _get_altimeter_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, CsvDataLocation]:
        if timestamp is None:
            return self._get_csv_data(iterator)
        else:
            return self._get_csv_data(iterator, timestamp)

    def _get_gps_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, CsvDataLocation]:
        if timestamp is None:
            return self._get_csv_data(iterator)
        else:
            return self._get_csv_data(iterator, timestamp)

    def _get_vrs_gps_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, CsvDataLocation]:
        if timestamp is None:
            return self._get_csv_data(iterator)
        else:
            return self._get_csv_data(iterator, timestamp)

    def _get_sick_back_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, BinaryDataLocation]:
        if timestamp is None:
            return self._get_bin_data(self.sick_back, iterator)
        else:
            return self._get_bin_data(self.sick_back, iterator, timestamp)

    def _get_sick_middle_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, BinaryDataLocation]:
        if timestamp is None:
            return self._get_bin_data(self.sick_middle, iterator)
        else:
            return self._get_bin_data(self.sick_middle, iterator, timestamp)

    def _get_velodyne_left_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, BinaryDataLocation]:
        if timestamp is None:
            return self._get_bin_data(self.velodyne_left, iterator)
        else:
            return self._get_bin_data(self.velodyne_left, iterator, timestamp)

    def _get_velodyne_right_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, BinaryDataLocation]:
        if timestamp is None:
            return self._get_bin_data(self.velodyne_right, iterator)
        else:
            return self._get_bin_data(self.velodyne_right, iterator, timestamp)

    def _get_stereo_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, StereoImgDataLocation]:
        if timestamp is None:
            return self._get_img_data(iterator)
        else:
            return self._get_img_data(iterator, timestamp)

    @staticmethod
    def _read_bin(file: Path) -> npt.NDArray[np.float32]:
        """Reads a binary file with Single-precision floating-point data (float32).

        Args:
            file (Path): binary file to be read.

        Returns:
            numpy.NDArray[np.float32]: array of single-precision floating-point data.
        """
        with open(file, "rb") as f:
            data = np.fromfile(f, np.float32)
            return data

    @staticmethod
    def _get_measurement(iterator: FileIterator) -> tuple[Message, CsvDataLocation]:
        """Iterates once with a given iterator.

        Args:
            iterator (FileIterator): iterator for sensor stamp ".csv" file.

        Returns:
            tuple[Message, CsvDataLocation]: message and location in CSV data file.
        """
        try:
            line = next(iterator)
        except StopIteration:
            msg = f"File: {iterator.file} has been exhausted."
            logger.critical(msg)
            raise
        else:
            position: int = iterator.position
            timestamp: str = line[0]
            data: tuple[str, ...] = tuple(line[1:])
            message = Message(timestamp, data)
            location = CsvDataLocation(iterator.file, position)
            return message, location

    def _find_measurement(self, iterator: FileIterator, timestamp: int) -> list[str]:
        """Iterates over file and finds the line with the given timestamp.

        Args:
            iterator (Iterator[tuple[int, tuple[str, ...]]]): iterator of tuple.
            timestamp (int): timestamp.

        Raises:
            StopIteration: if no line with the given timestamp in a file.

        Returns:
            tuple[int, tuple[str, ...]]: line number and line as tuple of strings.
        """
        current_timestamp: int = self._INCORRECT_TIMESTAMP
        line: list[str] = []
        while current_timestamp != timestamp:
            try:
                line = next(iterator)
            except StopIteration:
                msg = f"Iterator {iterator} has been exhausted."
                logger.error(msg)
                raise StopIteration(msg)
            else:
                timestamp_str: str = line[0]
                current_timestamp = as_int(timestamp_str)
        return line

    def _get_image(self, timestamp: int) -> tuple[Message, StereoImgDataLocation]:
        """Gets an image for a sensor with the given name and the timestamp.

        Args:
            timestamp (int): timestamp.
        Raises:
            ExternalModuleException: when OpenCV failed to read an image with opencv.imread() method.

        Returns:
            tuple[Message, StereoImgDataLocation]: message with raw stereo images and timestamp;
                                                   location of images
        """
        timestamp_str: str = str(timestamp)
        timestamp_path: Path = Path(timestamp_str)

        left_img_file = self._stereo_left_data_dir / timestamp_path
        right_img_file = self._stereo_right_data_dir / timestamp_path
        left_img_file = left_img_file.with_suffix(self._IMAGE_EXTENSION)
        right_img_file = right_img_file.with_suffix(self._IMAGE_EXTENSION)
        try:
            left_img = Image.open(left_img_file)
            right_img = Image.open(right_img_file)
        except Exception:
            msg = f"Can not read images: {left_img_file}, {right_img_file}"
            logger.critical(msg)
            raise ExternalModuleException(msg)

        message = Message(timestamp_str, (left_img, right_img))
        location = StereoImgDataLocation((left_img_file, right_img_file))
        return message, location

    @overload
    def _get_csv_data(self, iterator: FileIterator) -> tuple[Message, CsvDataLocation]:
        """
        @overload.
        Gets sensor`s measurement from csv file for the given sensor sequantially with iterator.

        Args:
            iterator (FileIterator): iterator for sensor stamp ".csv" file.

        Returns:
            tuple[Message, CsvDataLocation]: message with data and timestamp;
                                             measurement location.
        """

        message, location = self._get_measurement(iterator)
        return message, location

    @overload
    def _get_csv_data(
        self, iterator: FileIterator, timestamp: int
    ) -> tuple[Message, CsvDataLocation]:
        """
        @overload.
        Gets sensor`s measurement from csv file for the given sensor and the timestamp.

        Args:
            timestamp (int): timestamp of a measurement.
        Returns:
            tuple[Message, CsvDataLocation]: message with data and timestamp;
                                             measurement location.
        """
        try:
            line = self._find_measurement(iterator, timestamp)
        except StopIteration:
            msg = f"Could not find measurement with timestamp={timestamp} in {iterator.file}"
            logger.critical(msg)
            raise ItemNotFoundError(msg)
        message = Message(line[0], tuple(line[1:]))
        location = CsvDataLocation(iterator.file, iterator.position)
        return message, location

    @dispatch
    def _get_csv_data(self, iterator=None, timestamp=None):
        """
        @overload.

        Gets sensor`s measurement from csv file.

        Calls:
            1.  Args:
                    sensor (Sensor): sensor to get measurement for:
                    From current iterator position.
            2.  Args:
                    sensor (Sensor): sensor to get measurement for.
                    timestamp (int): timestamp of a measurement.
        """

    @overload
    def _get_bin_data(
        self, sensor_name: str, iterator: FileIterator
    ) -> tuple[Message, BinaryDataLocation]:
        """
        @overload.
        Gets sensor`s measurement from binary file for the given sensor sequantially with iterator.

        Args:
            sensor_name (str): name of sensor to get method for.

        Returns:
            tuple[Message, BinaryDataLocation]: message with data and timestamp;
                                                measurement location.
        """

        try:
            line = next(iterator)
        except StopIteration:
            msg = f"File {iterator.file} has been exhausted"
            logger.critical(msg)
            raise
        else:
            timestamp: str = str(line[0])
            timestamp_path: Path = Path(timestamp)
            file: Path = self._lidars_table[sensor_name] / timestamp_path
            file = file.with_suffix(self._BINARY_EXTENSION)
            raw_data: npt.NDArray[np.float32] = self._read_bin(file)
            raw_data_tuple: tuple[float, ...] = tuple(raw_data)
            message = Message(timestamp, raw_data_tuple)
            location = BinaryDataLocation(file)
            return message, location

    @overload
    def _get_bin_data(
        self, sensor_name: str, iterator: FileIterator, timestamp: int
    ) -> tuple[Message, BinaryDataLocation]:
        """
        @overload.
        Gets sensor`s measurement from binary file for the given sensor and the timestamp.

        Args:
            sensor_name (str): name of sensor to get method for.
            timestamp (int): timestamp of a measurement.

        Returns:
            tuple[Message, BinaryDataLocation]: message with data and timestamp;
                                                measurement location.
        """

        timestamp_str: str = str(timestamp)
        timestamp_path: Path = Path(timestamp_str)
        file: Path = self._lidars_table[sensor_name] / timestamp_path
        file = file.with_suffix(self._BINARY_EXTENSION)
        raw_data = self._read_bin(file)
        raw_data_tuple = tuple(raw_data)
        message = Message(timestamp_str, raw_data_tuple)
        location = BinaryDataLocation(file)
        return message, location

    @dispatch
    def _get_bin_data(self, sensor=None, iterator=None, timestamp=None):
        """
        @overload.

        Gets sensor`s measurement from binary file.

        Calls:
            1.  Args:
                    sensor (Sensor): sensor to get measurement for:
                    From current iterator position.
            2.  Args:
                    sensor (Sensor): sensor to get measurement for.
                    timestamp (int): timestamp of a measurement.
        """

    @overload
    def _get_img_data(self, iterator: FileIterator) -> tuple[Message, StereoImgDataLocation]:
        """
        @overload.
        Gets sensor`s measurement from a png file for the given sensor with the iterator sequentially.

        Args:
            iterator (FileIterator): iterator for sensor stamp ".csv" file.

        Returns:
            tuple[Message, StereoImgDataLocation]: message with data and timestamp;
                                                   measurement location.
        """
        try:
            line = next(iterator)
        except StopIteration:
            msg = f"File {iterator.file} has been exhausted"
            logger.critical(msg)
            raise
        else:
            timestamp: int = as_int(line[0])
            message, location = self._get_image(timestamp)
            return message, location

    @overload
    def _get_img_data(
        self, iterator: FileIterator, timestamp: int
    ) -> tuple[Message, StereoImgDataLocation]:
        """
        @overload.
        Gets sensor`s measurement from png file for the given sensor and the timestamp.

        Args:
            iterator (FileIterator): iterator for sensor stamp ".csv" file.
            timestamp (int): timestamp of a measurement.

        Returns:
            tuple[Message, StereoImgDataLocation]: message with data and timestamp;
                                                   measurement location.
        """

        message, location = self._get_image(timestamp)
        return message, location

    @dispatch
    def _get_img_data(self, iterator=None, timestamp=None):
        """
        @overload.

        Gets sensor`s measurement from .png file.

        Calls:
            1.  Args:
                    sensor (Sensor): sensor to get measurement for:
                    From current iterator position.
            2.  Args:
                    sensor (Sensor): sensor to get measurement for.
                    timestamp (int): timestamp of a measurement.
        """

    def get_data(
        self, sensor_name: str, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, Location]:
        """
        @overload.
        Gets data for the given sensor sequentially based on its iterator.

        Args:
            timestamp (int): timestamp of a measurement.
            iterator (FileIterator): iterator for sensor stamp ".csv" file.
            sensor_name (str): name of sensor to get data from.

        Returns:
            tuple[Message, Location]: message with data and timestamp;
                                            measurement location.
        """
        method: Callable = self._sensors_data_getters[sensor_name]
        try:
            message, location = method(iterator, timestamp)
        except ItemNotFoundError:
            msg = f"Could not find measurement with timestamp={timestamp} for sensor {sensor_name} in {iterator.file}"
            logger.critical(msg)
            raise ItemNotFoundError(msg)

        return message, location
