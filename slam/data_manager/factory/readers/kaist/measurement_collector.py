import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, overload

import numpy as np
import numpy.typing as npt
from PIL import Image
from plum import dispatch

from slam.data_manager.factory.element import Location
from slam.data_manager.factory.locations import (
    BinaryDataLocation,
    CsvDataLocation,
    StereoImgDataLocation,
)
from slam.data_manager.factory.readers.kaist.iterators import FileIterator
from slam.logger.logging_config import data_manager
from slam.utils.auxiliary_methods import as_int
from slam.utils.exceptions import ExternalModuleException, ItemNotFoundError

logger = logging.getLogger(data_manager)


@dataclass(frozen=True, eq=True)
class Message:
    """Message with the timestamp and data."""

    timestamp: str
    data: tuple


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
        """
        Args:
            lidar_data_dirs_table: "sensor name -> path to the directory with binary data files" table.
            stereo_data_dirs_table: "sensor name -> path to the directory with stereo images" table.
        """

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

    def get_data(
        self, sensor_name: str, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, Location]:
        """Gets data for the given sensor sequentially based on its iterator.

        Args:
            timestamp: timestamp of the measurement.

            iterator: iterator for sensor stamp ".csv" file.

            sensor_name: name of sensor to get data from.

        Returns:
            message with raw data and its location.

        Raises:
            ItemNotFoundError: no measurement with the timestamp in the file.
        """
        method: Callable = self._sensors_data_getters[sensor_name]
        try:
            message, location = method(iterator, timestamp)
        except ItemNotFoundError:
            msg = f"Could not find measurement with timestamp={timestamp} for sensor {sensor_name} in {iterator.file}"
            logger.critical(msg)
            raise ItemNotFoundError(msg)

        return message, location

    @staticmethod
    def read_bin(file: Path) -> np.ndarray:
        """Reads binary file with Single-precision floating-point data (float32).

        Args:
            file: path to binary file.

        Returns:
            array[N] (np.ndarray[np.float32]) of single-precision floating-point data.
        """
        with open(file, "rb") as f:
            data = np.fromfile(f, np.float32)
            return data

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
            return self._get_bin_data(self.sick_back, timestamp)

    def _get_sick_middle_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, BinaryDataLocation]:
        if timestamp is None:
            return self._get_bin_data(self.sick_middle, iterator)
        else:
            return self._get_bin_data(self.sick_middle, timestamp)

    def _get_velodyne_left_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, BinaryDataLocation]:
        if timestamp is None:
            return self._get_bin_data(self.velodyne_left, iterator)
        else:
            return self._get_bin_data(self.velodyne_left, timestamp)

    def _get_velodyne_right_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, BinaryDataLocation]:
        if timestamp is None:
            return self._get_bin_data(self.velodyne_right, iterator)
        else:
            return self._get_bin_data(self.velodyne_right, timestamp)

    def _get_stereo_data(
        self, iterator: FileIterator, timestamp: int | None = None
    ) -> tuple[Message, StereoImgDataLocation]:
        if timestamp is None:
            return self._get_img_data(iterator)
        else:
            return self._get_img_data(iterator, timestamp)

    @staticmethod
    def _get_measurement(iterator: FileIterator) -> tuple[Message, CsvDataLocation]:
        """Gets the next measurement for the given iterator.

        Args:
            iterator: iterator for sensor stamp ".csv" file.

        Returns:
            message and location in .csv file.

        Raises:
            StopIteration: the file iterator has been exhausted.
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
        """Finds the line with the given timestamp by iterating the given iterator.

        Args:
            iterator: file iterator.

            timestamp (int): timestamp.

        Returns:
            raw data from .csv file as a list of strings.

        Raises:
            StopIteration: if no line with the given timestamp in a file.
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
        """Gets the image of the given timestamp.

        Args:
            timestamp (int): timestamp.

        Returns:
            message with images, location.

        Raises:
            ExternalModuleException: when PIL.Image failed to read an image.
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

        Gets sensor`s measurement from .csv file for the given sensor sequentially.

        Args:
            iterator (FileIterator): iterator for sensor stamp ".csv" file.

        Returns:
            message, location (tuple[Message, CsvDataLocation]).
        """

        message, location = self._get_measurement(iterator)
        return message, location

    @overload
    def _get_csv_data(
        self, iterator: FileIterator, timestamp: int
    ) -> tuple[Message, CsvDataLocation]:
        """
        @overload.

        Gets sensor`s measurement from .csv file for the given sensor and the timestamp.

        Args:
            timestamp (int): timestamp of the measurement.

        Returns:
            message, location (tuple[Message, CsvDataLocation]).

        Raises:
            ItemNotFoundError: no measurement with the timestamp in the file.
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

        Gets sensor`s measurement from .csv file.

        Calls:
            1.  Gets sensor`s measurement from .csv file for the given sensor sequentially.

                Args:
                    iterator (FileIterator): iterator for sensor stamp ".csv" file.

                Returns:
                    message, location tuple[Message, CsvDataLocation].

            2.  Gets sensor`s measurement from .csv file for the given sensor and the timestamp.

                Args:
                    timestamp (int): timestamp of the measurement.

                Returns:
                    message, location (tuple[Message, CsvDataLocation]).

                Raises:
                    ItemNotFoundError: no measurement with the timestamp in the file.
        """

    @overload
    def _get_bin_data(
        self, sensor_name: str, iterator: FileIterator
    ) -> tuple[Message, BinaryDataLocation]:
        """
        @overload.

        Gets sensor`s measurement from binary file for the given sensor sequentially.

        Args:
            sensor_name (str): name of sensor to get data for.

            iterator (FileIterator): iterator for sensor stamp ".csv" file.

        Returns:
            message, location (tuple[Message, BinaryDataLocation]).

        Raises:
            StopIteration: the file iterator has been exhausted.
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
            raw_data: npt.NDArray[np.float32] = self.read_bin(file)
            raw_data_tuple: tuple[float, ...] = tuple(raw_data)
            message = Message(timestamp, raw_data_tuple)
            location = BinaryDataLocation(file)
            return message, location

    @overload
    def _get_bin_data(self, sensor_name: str, timestamp: int) -> tuple[Message, BinaryDataLocation]:
        """
        @overload.

        Gets sensor`s measurement from binary file for the given sensor and the timestamp.

        Args:
            sensor_name (str): name of sensor to get data for.

            timestamp (int): timestamp of a measurement.

        Returns:
            message, location (tuple[Message, BinaryDataLocation]).
        """

        timestamp_str: str = str(timestamp)
        timestamp_path: Path = Path(timestamp_str)
        file: Path = self._lidars_table[sensor_name] / timestamp_path
        file = file.with_suffix(self._BINARY_EXTENSION)
        raw_data = self.read_bin(file)
        raw_data_tuple = tuple(raw_data)
        message = Message(timestamp_str, raw_data_tuple)
        location = BinaryDataLocation(file)
        return message, location

    @dispatch
    def _get_bin_data(self, sensor_name=None, timestamp=None):
        """
        @overload.

        Gets sensor`s measurement from binary file.

        Calls:
            1.  Gets sensor`s measurement from binary file for the given sensor sequentially.

                Args:
                    sensor_name (str): name of sensor to get data for.

                    iterator (FileIterator): iterator for sensor stamp ".csv" file.

                Returns:
                    message, location (tuple[Message, BinaryDataLocation]).

                Raises:
                    StopIteration: the file iterator has been exhausted.

            2.  Gets sensor`s measurement from binary file for the given sensor and the timestamp.

                Args:
                    sensor_name (str): name of sensor to get data for.

                    timestamp (int): timestamp of a measurement.

                Returns:
                    message, location (tuple[Message, BinaryDataLocation]).

                Returns:
                    message, location (tuple[Message, BinaryDataLocation]).
        """

    @overload
    def _get_img_data(self, iterator: FileIterator) -> tuple[Message, StereoImgDataLocation]:
        """
        @overload.

        Gets sensor`s measurement from .png file for the given sensor sequentially.

        Args:
            iterator (FileIterator): iterator for sensor stamp ".csv" file.

        Returns:
            message, location (tuple[Message, StereoImgDataLocation]).

        Raises:
            StopIteration: the file iterator has been exhausted.
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
            message, location (tuple[Message, StereoImgDataLocation]).
        """

        message, location = self._get_image(timestamp)
        return message, location

    @dispatch
    def _get_img_data(self, iterator=None, timestamp=None):
        """
        @overload.

        Gets sensor`s measurement from .png file.

        Calls:
            1.  Gets sensor`s measurement from .png file for the given sensor sequentially.

                Args:
                    iterator (FileIterator): iterator for sensor stamp ".csv" file.

                Returns:
                    message, location (tuple[Message, StereoImgDataLocation]).

                Raises:
                    StopIteration: the file iterator has been exhausted.

            2.  Gets sensor`s measurement from png file for the given sensor and the timestamp.

                Args:
                    iterator (FileIterator): iterator for sensor stamp ".csv" file.

                    timestamp (int): timestamp of a measurement.

                Returns:
                    message, location (tuple[Message, StereoImgDataLocation]).

                Returns:
                    message, location (tuple[Message, StereoImgDataLocation]).
        """
