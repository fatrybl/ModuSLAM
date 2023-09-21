import logging

from dataclasses import InitVar, dataclass, field
from collections.abc import Iterator, Callable
from csv import reader as csv_reader
from pathlib import Path
from typing import Any, Type

from cv2 import imread, IMREAD_COLOR
from plum import dispatch

from configs.paths.DEFAULT_FILE_PATHS import KaistDataset
from slam.data_manager.factory.readers.element_factory import Location
from slam.setup_manager.sensor_factory.sensors import Sensor

logger = logging.getLogger(__name__)


@dataclass
class Message:
    timestamp: str
    data: list[str] | bytes | Any


@dataclass
class FileIterator:
    sensor_name: str
    file: Path
    iterator: Iterator[tuple[int, list[str]]]


@dataclass
class BinaryDataLocation(Location):
    file: Path


@dataclass
class StereoImgDataLocation(Location):
    files: list[Path] = field(default_factory=list, metadata={
                              'unit': 'list of Path-objects'})


@dataclass
class CsvDataLocation(Location):
    file: Path
    position: int


@dataclass(frozen=True)
class SensorNames:
    """
    Sensors` names must match with names in data_manager.yaml and data_readers.yaml
    """
    imu: str = 'imu'
    fog: str = 'fog'
    encoder: str = 'encoder'
    altimeter: str = 'altimeter'
    gps: str = 'gps'
    vrs: str = 'vrs'
    sick_back: str = 'sick_back'
    sick_middle: str = 'sick_middle'
    velodyne_left: str = 'velodyne_left'
    velodyne_right: str = 'velodyne_right'
    stereo: str = 'stereo'


@dataclass
class SensorIterators:
    directory: InitVar[Path]
    init: InitVar[Callable[[Path], Iterator[tuple[int, list[str]]]]]

    imu: FileIterator = field(init=False)
    fog: FileIterator = field(init=False)
    encoder: FileIterator = field(init=False)
    altimeter: FileIterator = field(init=False)
    gps: FileIterator = field(init=False)
    vrs: FileIterator = field(init=False)

    def __post_init__(self, directory: Path, init: Callable[[Path], Iterator[tuple[int, list[str]]]]):
        file = directory / KaistDataset.imu_data_file.value
        self.imu = FileIterator(SensorNames.imu, file, init(file))
        file = directory / KaistDataset.fog_data_file.value
        self.fog = FileIterator(SensorNames.fog, file, init(file))
        file = directory / KaistDataset.encoder_data_file.value
        self.encoder = FileIterator(SensorNames.encoder, file, init(file))
        file = directory / KaistDataset.altimeter_data_file.value
        self.altimeter = FileIterator(SensorNames.altimeter, file, init(file))
        file = directory / KaistDataset.gps_data_file.value
        self.gps = FileIterator(SensorNames.gps, file, init(file))
        file = directory / KaistDataset.vrs_gps_data_file.value
        self.vrs = FileIterator(SensorNames.vrs, file, init(file))

    def has_iterator_for(self, sensor: Type[Sensor]) -> bool:
        sensor_name: str = sensor.name
        class_names = self.__dataclass_fields__.keys()
        for s in class_names:
            if s == sensor_name:
                return True
        return False


class MeasurementCollector():
    def __init__(self, dataset_dir: Path):
        self._dataset_dir: Path = dataset_dir
        self._iterators = SensorIterators(
            self._dataset_dir, self._init_iterator)

    @property
    def sensor_iterators(self) -> SensorIterators:
        return self._iterators

    @sensor_iterators.setter
    def sensor_iterators(self, value: SensorIterators):
        self._iterators = value

    def _reset_iterators(self) -> None:
        self._iterators = SensorIterators(
            self._dataset_dir, self._init_iterator)

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
        current_timestamp: int = -1
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
    def get_imu(self) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.imu
        return self._iterate(it)

    @dispatch
    def get_imu(self, timestamp: int) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.imu
        position, line = self._find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def get_fog(self) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.fog
        return self._iterate(it)

    @dispatch
    def get_fog(self, timestamp: int) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.fog
        position, line = self._find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def get_encoder(self) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.encoder
        return self._iterate(it)

    @dispatch
    def get_encoder(self, timestamp: int) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.encoder
        position, line = self._find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def get_gps(self) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.gps
        return self._iterate(it)

    @dispatch
    def get_gps(self, timestamp: int) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.gps
        position, line = self._find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def get_vrs_gps(self) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.vrs
        return self._iterate(it)

    @dispatch
    def get_vrs_gps(self, timestamp: int) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.vrs
        position, line = self._find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    @dispatch
    def get_altimeter(self) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.altimeter
        return self._iterate(it)

    @dispatch
    def get_altimeter(self, timestamp: int) -> tuple[Message, CsvDataLocation]:
        it = self._iterators.altimeter
        position, line = self._find_in_file(it.iterator, timestamp)
        message = Message(line[0], line[1:])
        location = CsvDataLocation(it.file, position)
        return message, location

    def _get_lidar(self, timestamp: int, dir: Path) -> tuple[Message, BinaryDataLocation]:
        f_name = str(timestamp)
        file: Path = self._dataset_dir / dir / f_name
        file = file.with_suffix('.bin')
        message = self._read_bin(file)
        location = BinaryDataLocation(file)
        return message, location

    def get_lidar_2D_sick_back(self, timestamp: int) -> tuple[Message, BinaryDataLocation]:
        dir: Path = KaistDataset.lidar_2D_back_dir.value
        return self._get_lidar(timestamp, dir)

    def get_lidar_2D_sick_middle(self, timestamp: int) -> tuple[Message, BinaryDataLocation]:
        dir: Path = KaistDataset.lidar_2D_middle_dir.value
        return self._get_lidar(timestamp, dir)

    def get_lidar_3D_velodyne_left(self, timestamp: int) -> tuple[Message, BinaryDataLocation]:
        dir: Path = KaistDataset.lidar_3D_left_dir.value
        return self._get_lidar(timestamp, dir)

    def get_lidar_3D_velodyne_right(self, timestamp: int) -> tuple[Message, BinaryDataLocation]:
        dir: Path = KaistDataset.lidar_3D_right_dir.value
        return self._get_lidar(timestamp, dir)

    def get_stereo(self, timestamp: int) -> tuple[Message, StereoImgDataLocation]:
        f_name = str(timestamp)
        left_camera_dir: Path = self._dataset_dir / \
            KaistDataset.stereo_left_data_dir.value
        right_camera_dir: Path = self._dataset_dir / \
            KaistDataset.stereo_right_data_dir.value

        left_img_file = self._dataset_dir / left_camera_dir / f_name
        right_img_file = self._dataset_dir / right_camera_dir / f_name
        left_img_file = left_img_file.with_suffix('.png')
        right_img_file = right_img_file.with_suffix('.png')

        left_img = imread(left_img_file.as_posix(), IMREAD_COLOR)
        right_img = imread(right_img_file.as_posix(), IMREAD_COLOR)

        message = Message(f_name, [left_img, right_img])
        location = StereoImgDataLocation([left_img_file, right_img_file])

        return message, location

    def _get_reader(self, sensor: Type[Sensor]) -> Callable[[str | int | None], tuple[Message, Type[Location]]]:
        if sensor.name == SensorNames.imu:
            return self.get_imu
        elif sensor.name == SensorNames.fog:
            return self.get_fog
        elif sensor.name == SensorNames.encoder:
            return self.get_encoder
        elif sensor.name == SensorNames.gps:
            return self.get_gps
        elif sensor.name == SensorNames.vrs:
            return self.get_vrs_gps
        elif sensor.name == SensorNames.altimeter:
            return self.get_altimeter
        elif sensor.name == SensorNames.sick_back:
            return self.get_lidar_2D_sick_back
        elif sensor.name == SensorNames.sick_middle:
            return self.get_lidar_2D_sick_middle
        elif sensor.name == SensorNames.velodyne_left:
            return self.get_lidar_3D_velodyne_left
        elif sensor.name == SensorNames.velodyne_right:
            return self.get_lidar_3D_velodyne_right
        elif sensor.name == SensorNames.stereo:
            return self.get_stereo
        else:
            logger.critical(
                f"no method to parse data for sensor: {sensor} of type: {type(sensor)}")
            raise KeyError

    def get_data(self, sensor: Type[Sensor], timestamp: str) -> tuple[Message, Type[Location]]:
        data_reader = self._get_reader(sensor)
        if self._iterators.has_iterator_for(sensor):
            message, location = data_reader()
        else:
            message, location = data_reader(timestamp)
        return message, location

    def get_data_of_element(self, sensor: Type[Sensor], timestamp: int) -> Message:
        self._reset_iterators()
        data_reader = self._get_reader(sensor)
        message, __ = data_reader(timestamp)
        return message
