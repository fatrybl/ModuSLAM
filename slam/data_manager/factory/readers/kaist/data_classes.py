import logging

from dataclasses import dataclass, field, InitVar
from pathlib import Path
from typing import Any, Iterator, Callable
from configs.system.data_manager.datasets.kaist import Pair

from slam.data_manager.factory.readers.element_factory import Location


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Message:
    timestamp: str
    data: Any


@dataclass(frozen=True)
class FileIterator:
    sensor_name: str
    file: Path
    iterator: Iterator[tuple[int, list[str]]]


@dataclass(frozen=True)
class Storage:
    sensor_name: str
    path: Path


@dataclass(frozen=True)
class BinaryDataLocation(Location):
    file: Path


@dataclass(frozen=True)
class StereoImgDataLocation(Location):
    files: list[Path] = field(metadata={'unit': 'list of img paths'})


@dataclass(frozen=True)
class CsvDataLocation(Location):
    file: Path
    position: int


@dataclass
class SensorIterators:
    iterable_locations: InitVar[list[Pair]]
    init_method: InitVar[Callable[[Path], Iterator[tuple[int, list[str]]]]]

    iterators: set[FileIterator] = field(default_factory=lambda: set())

    def __post_init__(self, iterable_locations: list[Pair], init: Callable[[Path], Iterator[tuple[int, list[str]]]]):
        for pair in iterable_locations:
            name: str = pair.sensor_name
            location: Path = pair.location
            iterator: Iterator[tuple[int, list[str]]] = init(location)
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

    storages: set[Storage] = field(default_factory=lambda: set())

    def __post_init__(self, sensors_locations: list[Pair]):
        for s in sensors_locations:
            item = Storage(s.sensor_name, s.location)
            self.storages.add(item)

    def get_data_location(self, sensor_name: str):
        for s in self.storages:
            if s.sensor_name == sensor_name:
                return s
        msg = f'No Storage for {sensor_name} in set of {self.storages}'
        logger.critical(msg)
        raise ValueError(msg)
