import logging

from dataclasses import InitVar, dataclass, field
from collections.abc import Iterator, Callable
from csv import reader as csv_reader
from pathlib import Path
from typing import Any, Type

from cv2 import imread, IMREAD_COLOR
from plum import dispatch

from configs.paths.DEFAULT_FILE_PATHS import KaistDataset
from configs.system.data_manager.datasets.kaist import Pair
from slam.data_manager.factory.readers.element_factory import Location
from slam.setup_manager.sensor_factory.sensors import Altimeter, Encoder, Fog, Gps, Imu, Lidar2D, Lidar3D, Sensor, StereoCamera, VrsGps

logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=True)
class Message:
    timestamp: str
    data: list[str] | bytes | Any


@dataclass(frozen=True, eq=True)
class FileIterator:
    sensor_name: str
    file: Path
    iterator: Iterator[tuple[int, list[str]]]


@dataclass(frozen=True, eq=True)
class SensorStorage:
    sensor_name: str
    path: Path


@dataclass(frozen=True, eq=True)
class BinaryDataLocation(Location):
    file: Path


@dataclass(frozen=True, eq=True)
class StereoImgDataLocation(Location):
    files: list[Path] = field(default_factory=list, metadata={
                              'unit': 'list of Path-objects'})


@dataclass(frozen=True, eq=True)
class CsvDataLocation(Location):
    file: Path
    position: int


@dataclass
class SensorIterators:
    directory: InitVar[Path]
    iterable_locations: InitVar[list[Pair]]
    init: InitVar[Callable[[Path], Iterator[tuple[int, list[str]]]]]

    iterators: set[FileIterator] = field(default_factory=lambda: set())

    def __post_init__(self, directory: Path, iterable_locations: list[Pair], init: Callable[[Path], Iterator[tuple[int, list[str]]]]):
        for pair in iterable_locations:
            name = pair.sensor_name
            location = directory / pair.location
            iterator = init(location)
            file_iter = FileIterator(name,
                                     location,
                                     iterator)
            self.iterators.add(file_iter)

    def get_file_iterator(self, sensor_name: str):
        for it in self.iterators:
            if it.sensor_name == sensor_name:
                return it
        msg = f'No FileIterator for {sensor_name} in set of {self.iterators}'
        logger.critical(msg)
        raise ValueError(msg)


@dataclass(frozen=True, eq=True)
class DataStorage:
    sensors_locations: InitVar[list[Pair]]

    storages: set[SensorStorage] = field(default_factory=lambda: set())

    def __post_init__(self, sensors_locations: list[Pair]):
        for s in sensors_locations:
            item = SensorStorage(s.sensor_name, s.location)
            self.storages.add(item)

    def get_data_location(self, sensor_name: str):
        for s in self.storages:
            if s.sensor_name == sensor_name:
                return s
        msg = f'No Storage for {sensor_name} in set of {self.storages}'
        logger.critical(msg)
        raise ValueError(msg)


class MeasurementCollector():

    INCORRECT_TIMESTAMP: int = -1
    IMAGE_EXTENSION: str = '.png'

    def __init__(self, dataset_dir: Path, iterable_files: list[Pair], data_dirs: list[Pair]):
        self._dataset_dir: Path = dataset_dir
        self._iterable_data_files: list[Pair] = iterable_files

        self._sensor_data_storages = DataStorage(data_dirs)
        self._sensor_data_iterators = SensorIterators(
            dataset_dir,
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
                logger.error(
                    f"Could not find measurement in file with timestamp={timestamp}")
                raise
            else:
                try:
                    current_timestamp = int(line[0])
                except ValueError:
                    logger.error(
                        f"Could not convert timestamp {line[0]} of type {type(line[0])} to integer")
                    raise

                return position, line

    def _iterate(self, it: FileIterator) -> tuple[Message, CsvDataLocation]:
        position, line = next(it.iterator)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def get_csv_data(self, sensor: Sensor) -> tuple[Message, CsvDataLocation]:
        it = self._sensor_data_iterators.get_file_iterator(sensor.name)
        message, location = self._iterate(it)
        return message, location

    @dispatch
    def get_csv_data(self, sensor: Sensor, timestamp: int) -> tuple[Message, CsvDataLocation]:
        it = self._sensor_data_iterators.get_file_iterator(sensor.name)
        position, line = self._find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def get_bin_data(self, sensor: Sensor) -> tuple[Message, BinaryDataLocation]:
        it = self._sensor_data_iterators.get_file_iterator(sensor.name)
        timestamp: str = next(it.iterator)
        storage: SensorStorage = self._sensor_data_storages.get_data_location(
            sensor.name)
        file: Path = storage.path / str(timestamp)
        file = file.with_suffix('.bin')
        message = self._read_bin(file)
        location = BinaryDataLocation(file)
        return message, location

    @dispatch
    def get_bin_data(self, sensor: Sensor, timestamp: str) -> tuple[Message, BinaryDataLocation]:
        storage: SensorStorage = self._sensor_data_storages.get_data_location(
            sensor.name)
        file: Path = storage.path / str(timestamp)
        file = file.with_suffix('.bin')
        message = self._read_bin(file)
        location = BinaryDataLocation(file)
        return message, location

    def get_img_data(self, sensor: StereoCamera) -> tuple[Message, StereoImgDataLocation]:
        it = self._sensor_data_iterators.get_file_iterator(sensor.name)
        __, timestamp = next(it.iterator)
        timestamp = timestamp[0]
        storage: SensorStorage = self._sensor_data_storages.get_data_location(
            sensor.name)

        left_camera_dir: Path = self._dataset_dir / \
            storage.path / KaistDataset.stereo_left_data_dir.value
        right_camera_dir: Path = self._dataset_dir / \
            storage.path / KaistDataset.stereo_right_data_dir.value

        left_img_file = left_camera_dir / timestamp
        right_img_file = right_camera_dir / timestamp
        left_img_file = left_img_file.with_suffix(self.IMAGE_EXTENSION)
        right_img_file = right_img_file.with_suffix(self.IMAGE_EXTENSION)

        left_img = imread(left_img_file.as_posix(), IMREAD_COLOR)
        right_img = imread(right_img_file.as_posix(), IMREAD_COLOR)

        message = Message(timestamp, [left_img, right_img])
        location = StereoImgDataLocation([left_img_file, right_img_file])

        return message, location

    @dispatch
    def _get_data_by_sensor(self, sensor: Sensor) -> tuple[Message, Type[Location]]:
        if isinstance(sensor, (Imu, Fog, Altimeter, Gps, VrsGps, Encoder)):
            message, location = self.get_csv_data(sensor)
            return message, location
        elif isinstance(sensor, (Lidar2D, Lidar3D)):
            message, location = self.get_bin_data(sensor)
            return message, location
        elif isinstance(sensor, (StereoCamera)):
            message, location = self.get_img_data(sensor)
            return message, location
        else:
            msg = f"no method to parse data for sensor: {sensor} of type: {type(sensor)}"
            logger.critical(msg)
            raise ValueError(msg)

    @dispatch
    def _get_data_by_sensor(self, sensor: Sensor, timestamp: int) -> tuple[Message, Type[Location]]:
        if isinstance(sensor, (Imu, Fog, Altimeter, Gps, VrsGps, Encoder)):
            message, location = self.get_csv_data(sensor, timestamp)
            return message, location
        elif isinstance(sensor, (Lidar2D, Lidar3D)):
            message, location = self.get_bin_data(sensor, str(timestamp))
            return message, location
        # elif isinstance(sensor, (StereoCamera)):
        #     return self.get_img_data
        else:
            logger.critical(
                f"no method to parse data for sensor: {sensor} of type: {type(sensor)}")
            raise KeyError

    @dispatch
    def get_data(self, sensor: Sensor) -> tuple[Message, Type[Location]]:
        message, location = self._get_data_by_sensor(sensor)
        return message, location

    @dispatch
    def get_data(self, sensor: Sensor, timestamp: int) -> tuple[Message, Type[Location]]:
        self._reset_iterators()
        message, location = self._get_data_by_sensor(sensor, timestamp)
        return message, location
