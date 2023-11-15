import logging
from collections.abc import Iterator
from csv import reader as csv_reader
from PIL import Image
from pathlib import Path
from typing import Callable, Type

import numpy as np
import numpy.typing as npt
from plum import dispatch
from slam.data_manager.factory.readers.data_reader import DataReader

from slam.data_manager.factory.readers.element_factory import Location
from slam.data_manager.factory.readers.kaist.data_classes import (
    BinaryDataLocation, CsvDataLocation, DataStorage, FileIterator,
    Message, SensorIterators, StereoImgDataLocation, Storage)
from slam.setup_manager.sensor_factory.sensors import (
    Altimeter, Encoder, Fog, Gps, Imu,
    Lidar2D, Lidar3D, Sensor, StereoCamera, VrsGps)
from slam.utils.auxiliary_methods import as_int
from slam.utils.exceptions import ExternalModuleException, FileNotValid

from configs.paths.kaist_dataset import KaistDatasetPathConfig
from configs.system.data_manager.batch_factory.datasets.kaist import PairConfig

logger = logging.getLogger(__name__)


class CsvFileGenerator:
    """
    Generator for a ".csv" file to read each row and row`s number in a file.
    """

    def __init__(self, file_path: Path):
        self.__file = open(file_path, 'r')
        self.__reader = csv_reader(self.__file)
        self.__count = -1

    def __next__(self) -> tuple[int, tuple[str, ...]]:
        try:
            line = next(self.__reader)
            line = tuple(line)
            self.__count += 1
            return self.__count, line

        except StopIteration:
            self.__file.close()
            raise

    def __iter__(self):
        return self


class MeasurementCollector():
    """ 
    Collects sensors` measurements from Kaist Urban Dataset.
    """

    INCORRECT_TIMESTAMP: int = -1
    IMAGE_EXTENSION: str = '.png'
    BINARY_EXTENSION: str = '.bin'

    def __init__(self, iterable_files: list[PairConfig], data_dirs: list[PairConfig]):
        """
        Args:
            iterable_files (tuple[Pair]): each Pair has <SENSOR_NAME> and <LOCATION>, 
                which corresponds to unique sensor name and its stamp file path.
            data_dirs (tuple[Pair]): each Pair has <SENSOR_NAME> and <LOCATION>, 
                which corresponds to unique sensor name and its data directory.
        """
        dirs: tuple[PairConfig, ...] = tuple(data_dirs)
        self._iterable_data_files: tuple[PairConfig, ...] = tuple(
            iterable_files)
        self._sensor_data_storages = DataStorage(dirs)
        self._sensor_data_iterators = SensorIterators(
            self._iterable_data_files,
            self._init_iterator)

    @property
    def iterators(self) -> set[FileIterator]:
        """ 
        Set of iterators for sensors` stamp files.
        """
        return self._sensor_data_iterators.iterators

    @iterators.setter
    def iterators(self, value: set[FileIterator]):
        self._sensor_data_iterators.iterators = value

    def reset_iterators(self) -> None:
        """
        Re-initialize all iterators
        """
        self._sensor_data_iterators = SensorIterators(
            self._iterable_data_files,
            self._init_iterator)

    def _init_iterator(self, file: Path) -> Iterator[tuple[int, tuple[str, ...]]]:
        """
        Initializes an iterator for a given file.

        Args:
            file (Path): file to be iterated.

        Yields:
            Iterator[tuple[int, tuple[str]]]: line number, tuple of string for each line in the file.
        """
        if DataReader.is_file_valid(file):
            return CsvFileGenerator(file)
        else:
            msg = f"file: {file} is not valid to initialize the iterator"
            logger.critical(msg)
            raise FileNotValid(msg)

    def __read_bin(self, file: Path) -> npt.NDArray[np.float32]:
        """
        Reads a binary file with Single-precision floating-point data (float32).

        Args:
            file (Path): binary file to be read.

        Returns:
            numpy.NDArray[np.float32]: array of single-precision floating-point data.
        """
        with open(file, 'rb') as f:
            data = np.fromfile(f, np.float32)
            return data

    def __find_in_file(self, iter: Iterator[tuple[int, tuple[str, ...]]], timestamp: int) -> tuple[int, tuple[str, ...]]:
        """
        Iterates over file and finds the line with the given timestamp.

        Args:
            iter (Iterator[tuple[int, tuple[str, ...]]]): iterator of tuple. 
            timestamp (int): timestamp.

        Raises:
            StopIteration: if no line with the given timestamp in a file.

        Returns:
            tuple[int, tuple[str, ...]]: line number and line as tuple of strings.
        """
        current_timestamp: int = self.INCORRECT_TIMESTAMP
        while current_timestamp != timestamp:
            try:
                position, line = next(iter)
            except StopIteration:
                msg = f"Could not find measurement with timestamp={timestamp}"
                logger.error(msg)
                raise StopIteration(msg)
            else:
                timestamp_str: str = line[0]
                current_timestamp = as_int(timestamp_str, logger)
        return position, line

    def __iterate(self, it: FileIterator) -> tuple[Message, CsvDataLocation]:
        """
        Iterates once with a given iterator.

        Args:
            it (FileIterator): iterator for sensor stamp ".csv" file.

        Returns:
            tuple[Message, CsvDataLocation]: message and location in CSV data file.
        """
        position, line = next(it.iterator)
        timestamp: str = line[0]
        data: tuple[str, ...] = line[1:]
        message = Message(timestamp, data)
        location = CsvDataLocation(it.file, position)
        return message, location

    def __update_iterator(self, iterator: Iterator[tuple[int, tuple[str, ...]]], timestamp: int) -> None:
        """ 
        Sets the iterator to the position of the given timestamp.

        Args:
            iterator (Iterator[tuple[int, tuple[str, ...]]]): to be set to the position.
            timestamp (int): timestamp.
        """
        __, __ = self.__find_in_file(iterator, timestamp)

    def _get_image(self, sensor_name: str, timestamp: int) -> tuple[Message, StereoImgDataLocation]:
        """ 
        Gets an image for a sensor with the given name and the timestamp.

        Args:
            sensor_name (str): name of sensor.
            timestamp (int): timestamp.
        Raises:
            ExternalModuleException: when OpenCV failed to read an image with opencv.imread() method.

        Returns:
            tuple[Message, StereoImgDataLocation]: message with raw stereo images and timestamp;
                                                   location of images
        """
        timestamp_str: str = str(timestamp)
        timestamp_path: Path = Path(timestamp_str)
        storage: Storage = self._sensor_data_storages.get_data_location(
            sensor_name)

        left_camera_dir: Path = storage.path / \
            KaistDatasetPathConfig.stereo_left_data_dir
        right_camera_dir: Path = storage.path / \
            KaistDatasetPathConfig.stereo_right_data_dir

        left_img_file = left_camera_dir / timestamp_path
        right_img_file = right_camera_dir / timestamp_path
        left_img_file = left_img_file.with_suffix(self.IMAGE_EXTENSION)
        right_img_file = right_img_file.with_suffix(self.IMAGE_EXTENSION)
        try:
            left_img = Image.open(left_img_file)
            right_img = Image.open(right_img_file)
        except:
            msg = f"Can not read images: {left_img_file}, {right_img_file}"
            logger.critical(msg)
            raise ExternalModuleException(msg)

        message = Message(timestamp_str, (left_img, right_img))
        location = StereoImgDataLocation((left_img_file, right_img_file))
        return message, location

    @dispatch
    def _get_csv_data(self, sensor: Sensor) -> tuple[Message, CsvDataLocation]:
        """ 
        Overloaded method.
        Gets sensor`s measurement from csv file for the given sensor sequantially with iterator.

        Args:
            sensor (Sensor): sensor to get measurement for.

        Returns:
            tuple[Message, CsvDataLocation]: message with data and timestamp; 
                                             measurement location.
        """
        it: FileIterator = self._sensor_data_iterators.get_file_iterator(
            sensor.name)
        message, location = self.__iterate(it)
        return message, location

    @dispatch
    def _get_csv_data(self, sensor: Sensor, timestamp: int) -> tuple[Message, CsvDataLocation]:
        """
        Overloaded method.
        Gets sensor`s measurement from csv file for the given sensor and the timestamp.

        Args:
            sensor (Sensor): sensor to get measurement for.
            timestamp (int): timestamp of a measurement.
        Returns:
            tuple[Message, CsvDataLocation]: message with data and timestamp; 
                                             measurement location.
        """
        it: FileIterator = self._sensor_data_iterators.get_file_iterator(
            sensor.name)
        position, line = self.__find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def _get_bin_data(self, sensor: Sensor) -> tuple[Message, BinaryDataLocation]:
        """
        Overloaded method.
        Gets sensor`s measurement from binary file for the given sensor sequantially with iterator.

        Args:
            sensor (Sensor): sensor to get measurement for.

        Returns:
            tuple[Message, BinaryDataLocation]: message with data and timestamp; 
                                                measurement location.
        """

        it: FileIterator = self._sensor_data_iterators.get_file_iterator(
            sensor.name)
        __, line = next(it.iterator)
        storage: Storage = self._sensor_data_storages.get_data_location(
            sensor.name)
        timestamp: str = str(line[0])
        timestamp_path: Path = Path(timestamp)
        file: Path = storage.path / timestamp_path
        file = file.with_suffix(self.BINARY_EXTENSION)
        raw_data: npt.NDArray[np.float32] = self.__read_bin(file)
        raw_data_tuple: tuple[float, ...] = tuple(raw_data)
        message = Message(timestamp, raw_data_tuple)
        location = BinaryDataLocation(file)
        return message, location

    @dispatch
    def _get_bin_data(self, sensor: Sensor, timestamp: int) -> tuple[Message, BinaryDataLocation]:
        """
        Overloaded method.
        Gets sensor`s measurement from binary file for the given sensor and the timestamp.

        Args:
            sensor (Sensor): sensor to get measurement for.
            timestamp (int): timestamp of a measurement.

        Returns:
            tuple[Message, BinaryDataLocation]: message with data and timestamp; 
                                                measurement location.
        """
        it: FileIterator = self._sensor_data_iterators.get_file_iterator(
            sensor.name)
        self.__update_iterator(it.iterator, timestamp)
        storage: Storage = self._sensor_data_storages.get_data_location(
            sensor.name)
        timestamp_str: str = str(timestamp)
        file: Path = storage.path / timestamp_str
        file = file.with_suffix(self.BINARY_EXTENSION)
        raw_data = self.__read_bin(file)
        raw_data = tuple(raw_data)
        message = Message(timestamp_str, raw_data)
        location = BinaryDataLocation(file)
        return message, location

    @dispatch
    def _get_img_data(self, sensor: StereoCamera) -> tuple[Message, StereoImgDataLocation]:
        """
        Overloaded method.
        Gets sensor`s measurement from a png file for the given sensor with the iterator sequantially.

        Args:
            sensor (StereoCamera): sensor to get measurement for.

        Returns:
            tuple[Message, StereoImgDataLocation]: message with data and timestamp; 
                                                   measurement location.
        """
        it: FileIterator = self._sensor_data_iterators.get_file_iterator(
            sensor.name)
        __, line = next(it.iterator)
        timestamp: int = as_int(line[0], logger)
        message, location = self._get_image(sensor.name, timestamp)
        return message, location

    @dispatch
    def _get_img_data(self, sensor: StereoCamera, timestamp: int) -> tuple[Message, StereoImgDataLocation]:
        """
        Overloaded method.
        Gets sensor`s measurement from png file for the given sensor and the timestamp.

        Args:
            sensor (StereoCamera): sensor to get measurement for.
            timestamp (int): timestamp of a measurement.

        Returns:
            tuple[Message, StereoImgDataLocation]: message with data and timestamp; 
                                                   measurement location.
        """
        it: FileIterator = self._sensor_data_iterators.get_file_iterator(
            sensor.name)
        self.__update_iterator(it.iterator, timestamp)
        message, location = self._get_image(sensor.name, timestamp)
        return message, location

    def __get_sensor_method(self, sensor: Type[Sensor]) -> Callable[..., tuple[Message, Type[Location]]]:
        """
        Gets sensor`s specific method based on given sensor`s type

        Args:
            sensor (Type[Sensor]): sensor to get method for.

        Raises:
            TypeError: if no method for given sensor`s type

        Returns:
            Callable[..., tuple[Message, Type[Location]]]: method to get raw sensor measurement.
        """
        if isinstance(sensor, (Imu, Fog, Altimeter, Gps, VrsGps, Encoder)):
            return self._get_csv_data
        elif isinstance(sensor, (Lidar2D, Lidar3D)):
            return self._get_bin_data
        elif isinstance(sensor, (StereoCamera)):
            return self._get_img_data
        else:
            msg = f"no method to parse data for sensor: {sensor} of type: {type(sensor)}"
            logger.critical(msg)
            raise TypeError(msg)

    @dispatch
    def get_data(self, sensor: Sensor) -> tuple[Message, Type[Location]]:
        """
        Overloaded method.
        Gets data for the given sensor sequantially based on its iterator.

        Args:
            sensor (Sensor): sensor to get method for.

        Returns:
            tuple[Message, Type[Location]]: message with data and timestamp; 
                                            measurement location.
        """
        method = self.__get_sensor_method(sensor)
        message, location = method(sensor)
        return message, location

    @dispatch
    def get_data(self, sensor: Sensor, timestamp: int) -> tuple[Message, Type[Location]]:
        """
        Overloaded method.
        Gets data for the given sensor and the timestamp.

        Args:
            sensor (Sensor): sensor to get method for.
            timestamp (int): timestamp of a measurement.

        Returns:
            tuple[Message, Type[Location]]: message with data and timestamp; 
                                            measurement location.
        """
        self.reset_iterators()
        method = self.__get_sensor_method(sensor)
        message, location = method(sensor, timestamp)
        return message, location
