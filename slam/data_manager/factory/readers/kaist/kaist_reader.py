import logging

from typing import Type
from dataclasses import dataclass
from csv import DictReader
from collections.abc import Iterator
from pathlib import Path

from plum import dispatch

from slam.data_manager.factory.readers.data_reader import DataReader, DataFlowState
from slam.data_manager.factory.readers.element_factory import Measurement
from slam.data_manager.factory.readers.kaist.measurement_collector import (
    MeasurementCollector, FileIterator, Message)
from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.exceptions import FileNotValid
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor
from configs.system.data_manager.datasets.kaist import Kaist
from configs.paths.kaist_dataset import KaistDataset

logger = logging.getLogger(__name__)


@dataclass
class KaistReaderState(DataFlowState):
    """
    Keeps iterators for each measurement. 
    """
    data_stamp_iterator: Iterator[dict[str, str]]
    sensors_iterators: set[FileIterator]


class KaistReader(DataReader):
    def __init__(self, cfg: Kaist):
        dataset_dir: Path = cfg.directory
        self.__collector = MeasurementCollector(
            dataset_dir, cfg.iterable_data_files, cfg.data_dirs)
        self.__sensor_order_file: Path = dataset_dir / \
            KaistDataset.sensor_data_dir / cfg.data_stamp_file
        self.__data_stamp_iterator: Iterator[dict[str, str]] = self.__init_iterator(
        )
        self.__current_iterators = KaistReaderState(
            self.__data_stamp_iterator,
            self.__collector.iterators)

    @property
    def current_state(self) -> KaistReaderState:
        return self.__current_iterators

    def __init_iterator(self) -> Iterator[dict[str, str]]:
        if (DataReader._is_file_valid(self.__sensor_order_file)):
            with open(self.__sensor_order_file, "r") as f:
                names = ["timestamp", "sensor_name"]
                reader = DictReader(f, fieldnames=names)
                for line in reader:
                    yield line
        else:
            logger.critical(
                f"file: {self.__sensor_order_file} is not valid to initialize the iterator")
            raise FileNotValid

    def __as_int(self, timestamp: str) -> int:
        try:
            return int(timestamp)
        except ValueError:
            logger.error(
                f"Could not convert timestamp {timestamp} of type {type(timestamp)} to string")
            raise

    @dispatch
    def get_element(self) -> Element | None:
        try:
            while True:
                line = next(self.__data_stamp_iterator)
                sensor = SensorFactory.name_to_sensor(line["sensor_name"])
                if sensor in SensorFactory.used_sensors:
                    break

        except StopIteration:
            msg = f"stopping iteration, {self.__sensor_order_file} has been processed"
            logger.info(msg)
            return None

        else:
            sensor: Type[Sensor] = SensorFactory.name_to_sensor(
                line["sensor_name"])
            timestamp: str = line["timestamp"]

            self.__collector.iterators = self.__current_iterators.sensors_iterators
            message, location = self.__collector.get_data(sensor)

            timestamp = self.__as_int(timestamp)
            measurement = Measurement(sensor, message.data)
            element = Element(timestamp,
                              measurement,
                              location)
            return element

    @dispatch
    def get_element(self, element: Element) -> Element:
        sensor: Type[Sensor] = element.measurement.sensor
        timestamp: int = element.timestamp
        message, __ = self.__collector.get_data(sensor, timestamp)

        measurement = Measurement(element.measurement.sensor, message.data)
        element = Element(element.timestamp,
                          measurement,
                          element.location)
        return element

    @dispatch
    def get_element(self, sensor: Type[Sensor], timestamp: int) -> Element:
        # 1) найти элемент с t0
        # 2) проинициализировать итератор с него
        # 3) итерироваться по нему.
        raise NotImplementedError
