import logging

from dataclasses import dataclass, field, InitVar
from pathlib import Path
from typing import Any, Iterator, Callable
from configs.system.data_manager.batch_factory.datasets.kaist import PairConfig

from slam.data_manager.factory.readers.element_factory import Location


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Message:
    """
    Message with a timestamp and any data.
    """
    timestamp: str
    data: tuple[Any, ...]


@dataclass(frozen=True)
class FileIterator:
    """
    Iterator for sensor`s stamp file.
    """
    sensor_name: str
    file: Path
    iterator: Iterator[tuple[int, tuple[str, ...]]]


@dataclass(frozen=True)
class Storage:
    """
    Storage for sensor`s data. For a directory with bin / png / ...
    """
    sensor_name: str
    path: Path


@dataclass(frozen=True)
class BinaryDataLocation(Location):
    """
    Binary data location.
    """
    file: Path


@dataclass(frozen=True)
class StereoImgDataLocation(Location):
    """
    Stereo data location. Stores paths as a tuple.
    """
    files: tuple[Path, ...] = field(metadata={'unit': 'tuple of img paths'})


@dataclass(frozen=True)
class CsvDataLocation(Location):
    """
    Csv data location: a file and position (line number) in a file.
    """
    file: Path
    position: int


@dataclass
class SensorIterators:
    """
    Iterators for sensors` data files.

    Raises:
        ValueError: No FileIterator found for the given sensor name.
    """
    iterable_locations: InitVar[tuple[PairConfig, ...]]
    init_method: InitVar[Callable[[Path],
                                  Iterator[tuple[int, tuple[str, ...]]]]]

    iterators: set[FileIterator] = field(default_factory=lambda: set())

    def __post_init__(self, iterable_locations: tuple[PairConfig, ...], init: Callable[[Path], Iterator[tuple[int, tuple[str, ...]]]]):
        for pair in iterable_locations:
            name: str = pair.sensor_name
            location: Path = pair.location
            iterator: Iterator[tuple[int, tuple[str, ...]]] = init(location)
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
    """
    Data storages for sensors` data of type .bin / .png / etc. 

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    sensors_locations: InitVar[tuple[PairConfig, ...]]

    storages: set[Storage] = field(default_factory=lambda: set())

    def __post_init__(self, sensors_locations: tuple[PairConfig, ...]):
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
