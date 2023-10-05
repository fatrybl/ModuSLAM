import logging

from collections.abc import Iterator
from csv import reader as csv_reader
from pathlib import Path
from typing import Type

from cv2 import imread, IMREAD_COLOR
from plum import dispatch

from configs.paths.kaist_dataset import KaistDataset
from configs.system.data_manager.datasets.kaist import Pair

from slam.data_manager.factory.readers.element_factory import Location
from slam.data_manager.factory.readers.kaist.data_classes import (
    BinaryDataLocation, CsvDataLocation, DataStorage, FileIterator,
    Message, SensorIterators, StereoImgDataLocation, Storage)
from slam.setup_manager.sensor_factory.sensors import (
    Altimeter, Encoder, Fog, Gps, Imu,
    Lidar2D, Lidar3D, Sensor, StereoCamera, VrsGps)
from slam.utils.auxiliary_methods import as_int

logger = logging.getLogger(__name__)


class MeasurementCollector():

    INCORRECT_TIMESTAMP: int = -1
    IMAGE_EXTENSION: str = '.png'
    BINARY_EXTENSION: str = '.bin'

    def __init__(self, iterable_files: list[Pair], data_dirs: list[Pair]):
        self._iterable_data_files: list[Pair] = iterable_files
        self._sensor_data_storages = DataStorage(data_dirs)
        self._sensor_data_iterators = SensorIterators(
            iterable_files,
            self._init_iterator)

    @property
    def iterators(self) -> set[FileIterator]:
        return self._sensor_data_iterators.iterators

    @iterators.setter
    def iterators(self, value: set[FileIterator]):
        self._sensor_data_iterators.iterators = value

    def _reset_iterators(self) -> None:
        self._sensor_data_iterators = SensorIterators(
            self._iterable_data_files,
            self._init_iterator)

    def _init_iterator(self, file: Path) -> Iterator[tuple[int, list[str]]]:
        with open(file, "r") as f:
            reader = csv_reader(f)
            for position, line in enumerate(reader):
                yield position, line

    def _read_bin(self, file: Path) -> Message:
        with open(file, 'rb') as f:
            line = f.read()
            return Message(file.stem, line)

    def _find_in_file(self, iter: Iterator[tuple[int, list[str]]], timestamp: int) -> tuple[int, list[str]] | None:
        current_timestamp: int = self.INCORRECT_TIMESTAMP
        while current_timestamp != timestamp:
            try:
                position, line = next(iter)
            except StopIteration:
                msg = f"Could not find measurement in file with timestamp={timestamp}"
                logger.error(msg)
                raise
            else:
                current_timestamp = as_int(line[0], logger)
                return position, line

    def _iterate(self, it: FileIterator) -> tuple[Message, CsvDataLocation]:
        position, line = next(it.iterator)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    def _get_image(self, sensor_name: str, timestamp: Path) -> tuple[Message, StereoImgDataLocation]:
        storage: Storage = self._sensor_data_storages.get_data_location(
            sensor_name)

        left_camera_dir: Path = storage.path / KaistDataset.stereo_left_data_dir
        right_camera_dir: Path = storage.path / KaistDataset.stereo_right_data_dir

        left_img_file = left_camera_dir / timestamp
        right_img_file = right_camera_dir / timestamp
        left_img_file = left_img_file.with_suffix(self.IMAGE_EXTENSION)
        right_img_file = right_img_file.with_suffix(self.IMAGE_EXTENSION)
        left_img = imread(left_img_file.as_posix(), IMREAD_COLOR)
        right_img = imread(right_img_file.as_posix(), IMREAD_COLOR)

        for img, path in zip([left_img, right_img], [left_img_file, right_img_file]):
            if img is None:
                msg = f"img with path {path} has not been read with OpenCV::IMREAD"
                logger.critical(msg)
                raise ValueError(msg)

        message = Message(timestamp, [left_img, right_img])
        location = StereoImgDataLocation([left_img_file, right_img_file])
        return message, location

    @dispatch
    def _get_csv_data(self, sensor: Sensor) -> tuple[Message, CsvDataLocation]:
        it = self._sensor_data_iterators.get_file_iterator(sensor.name)
        message, location = self._iterate(it)
        return message, location

    @dispatch
    def _get_csv_data(self, sensor: Sensor, timestamp: int) -> tuple[Message, CsvDataLocation]:
        it = self._sensor_data_iterators.get_file_iterator(sensor.name)
        position, line = self._find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def _get_bin_data(self, sensor: Sensor) -> tuple[Message, BinaryDataLocation]:
        it = self._sensor_data_iterators.get_file_iterator(sensor.name)
        __, line = next(it.iterator)
        storage: Storage = self._sensor_data_storages.get_data_location(
            sensor.name)
        timestamp: Path = Path(line[0])
        file: Path = storage.path / timestamp
        file = file.with_suffix(self.BINARY_EXTENSION)
        message = self._read_bin(file)
        location = BinaryDataLocation(file)
        return message, location

    @dispatch
    def _get_bin_data(self, sensor: Sensor, timestamp: int) -> tuple[Message, BinaryDataLocation]:
        storage: Storage = self._sensor_data_storages.get_data_location(
            sensor.name)
        file: Path = storage.path / str(timestamp)
        file = file.with_suffix(self.BINARY_EXTENSION)
        message = self._read_bin(file)
        location = BinaryDataLocation(file)
        return message, location

    @dispatch
    def _get_img_data(self, sensor: StereoCamera) -> tuple[Message, StereoImgDataLocation]:
        it = self._sensor_data_iterators.get_file_iterator(sensor.name)
        __, line = next(it.iterator)
        timestamp: Path = Path(line[0])
        message, location = self._get_image(sensor.name, timestamp)
        return message, location

    @dispatch
    def _get_img_data(self, sensor: StereoCamera, timestamp: int) -> tuple[Message, StereoImgDataLocation]:
        timestamp: Path = Path(str(timestamp))
        message, location = self._get_image(sensor.name, timestamp)
        return message, location

    @dispatch
    def _get_data_by_sensor(self, sensor: Sensor) -> tuple[Message, Type[Location]]:
        if isinstance(sensor, (Imu, Fog, Altimeter, Gps, VrsGps, Encoder)):
            message, location = self._get_csv_data(sensor)
            return message, location
        elif isinstance(sensor, (Lidar2D, Lidar3D)):
            message, location = self._get_bin_data(sensor)
            return message, location
        elif isinstance(sensor, (StereoCamera)):
            message, location = self._get_img_data(sensor)
            return message, location
        else:
            msg = f"no method to parse data for sensor: {sensor} of type: {type(sensor)}"
            logger.critical(msg)
            raise ValueError(msg)

    @dispatch
    def _get_data_by_sensor(self, sensor: Sensor, timestamp: int) -> tuple[Message, Type[Location]]:
        if isinstance(sensor, (Imu, Fog, Altimeter, Gps, VrsGps, Encoder)):
            message, location = self._get_csv_data(sensor, timestamp)
            return message, location
        elif isinstance(sensor, (Lidar2D, Lidar3D)):
            message, location = self._get_bin_data(sensor, timestamp)
            return message, location
        elif isinstance(sensor, (StereoCamera)):
            message, location = self._get_img_data(sensor, timestamp)
            return message, location
        else:
            msg = f"no method to parse data for sensor: {sensor} of type: {type(sensor)}"
            logger.critical(msg)
            raise ValueError(msg)

    @dispatch
    def get_data(self, sensor: Sensor) -> tuple[Message, Type[Location]]:
        message, location = self._get_data_by_sensor(sensor)
        return message, location

    @dispatch
    def get_data(self, sensor: Sensor, timestamp: int) -> tuple[Message, Type[Location]]:
        self._reset_iterators()
        message, location = self._get_data_by_sensor(sensor, timestamp)
        return message, location
