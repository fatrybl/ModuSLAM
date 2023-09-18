import logging

from typing import Type
from dataclasses import dataclass
from csv import DictReader
from collections.abc import Iterator
from plum import dispatch
from pathlib import Path

from slam.data_manager.factory.readers.data_reader import DataReader, DataFlowState
from slam.data_manager.factory.readers.element_factory import Measurement
from slam.data_manager.factory.readers.kaist.measurement_collector import MeasurementCollector, SensorIterators
from slam.data_manager.factory.readers.element_factory import Element
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths, KaistDataset
from slam.utils.config import Config
from slam.utils.exceptions import FileNotValid
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor

logger = logging.getLogger(__name__)


@dataclass
class KaistReaderState(DataFlowState):
    """
    Keeps iterators for each measurement. 
    """
    data_stamp: Iterator[dict[str, str]]
    sensors: SensorIterators


class KaistReader(DataReader):
    def __init__(self):
        cfg1: Config = Config.from_file(
            ConfigFilePaths.data_manager_config.value)
        cfg2: Config = Config.from_file(
            ConfigFilePaths.data_reader_config.value)
        dataset_dir: Path = Path(cfg1.attributes["data"]["dataset_directory"])
        self.__used_sensors: set[str] = set(cfg2.attributes["used_sensors"])
        self.__collector = MeasurementCollector(dataset_dir)
        self.__sensor_order_file: Path = dataset_dir / KaistDataset.data_stamp.value
        self.__data_stamp_iterator: Iterator[dict[str, str]] = self.__init_iterator(
        )
        self.__sensor_factory = SensorFactory()
        self.__current_iterators = KaistReaderState(
            self.__data_stamp_iterator,
            self.__collector.sensor_iterators)

    @property
    def current_state(self) -> KaistReaderState:
        return self.__current_iterators

    def __init_iterator(self) -> Iterator[dict[str, str]]:
        if (DataReader._is_file_valid(self.__sensor_order_file)):
            with open(self.__sensor_order_file, "r") as f:
                names = ["timestamp", "sensor"]
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
                if line["sensor"] in self.__used_sensors:
                    break

        except StopIteration:
            logger.info(
                "stopping iteration, data_stamp.csv has been processed")
            return None

        else:
            sensor: Type[Sensor] = self.__sensor_factory.name_to_sensor(
                line["sensor"])
            timestamp: str = line["timestamp"]

            self.__collector.sensor_iterators = self.__current_iterators.sensors
            message, location = self.__collector.get_data(sensor, timestamp)

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
        message = self.__collector.get_data_of_element(sensor, timestamp)

        measurement = Measurement(element.measurement.sensor, message.data)
        element = Element(element.timestamp,
                          measurement,
                          element.location)
        return element

    @dispatch
    def get_element(self, *args) -> Element:
        raise NotImplementedError
