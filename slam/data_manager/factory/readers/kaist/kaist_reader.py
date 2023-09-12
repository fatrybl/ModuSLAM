import logging

from csv import DictReader
from collections.abc import Iterator
from plum import dispatch
from pathlib import Path

from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Measurement
from slam.data_manager.factory.readers.kaist.measurement_collector import MeasurementCollector
from slam.data_manager.factory.readers.element_factory import Element
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths, KaistDataset
from slam.utils.config import Config
from slam.utils.exceptions import FileNotValid

logger = logging.getLogger(__name__)


class KaistReader(DataReader):
    def __init__(self) -> None:
        cfg1: Config = Config.from_file(
            ConfigFilePaths.data_manager_config.value)
        cfg2: Config = Config.from_file(
            ConfigFilePaths.data_reader_config.value)
        dataset_dir: Path = Path(cfg1.attributes["data"]["dataset_directory"])
        self.__used_sensors: list[str] = cfg2.attributes["kaist_reader"]["used_sensors"]
        self.__collector = MeasurementCollector(dataset_dir)
        self.__sensor_order_file: Path = dataset_dir / KaistDataset.data_stamp.value
        self.__iterator: Iterator[dict[str, str]] = self.__init_iterator()

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

    @dispatch
    def get_element(self) -> Element | None:
        try:
            while True:
                line = next(self.__iterator)
                if line["sensor"] in self.__used_sensors:
                    break
                else:
                    continue

        except StopIteration:
            logger.info(
                "stopping iteration, data_stamp.csv has been processed")
            return None

        else:
            message, location = self.__collector.get_data(line)
            sensor = line["sensor"]
            data = message["data"]

        try:
            timestamp = int(message["timestamp"])
        except ValueError:
            logger.error(
                f"Couldn't convert {timestamp} of type {type(timestamp)} to integer")
            return None
        else:
            measurement = Measurement(sensor, data)
            element = Element(timestamp,
                              measurement,
                              location)
            return element

    @dispatch
    def get_element(self, element: Element) -> Element:
        line = {"timestamp": element.timestamp,
                "sensor": element.measurement.sensor}
        message, location = self.__collector.get_data_of_element(line)
        data = message["data"]
        measurement = Measurement(element.measurement.sensor, data)
        element = Element(element.timestamp,
                          measurement,
                          element.location)
        return element

    @dispatch
    def get_element(self, element: dict) -> Element:
        raise NotImplementedError
