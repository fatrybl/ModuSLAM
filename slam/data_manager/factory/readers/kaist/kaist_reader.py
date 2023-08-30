import logging
import sys

from csv import DictReader
from plum import dispatch

from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Measurement
from slam.data_manager.factory.readers.kaist.measurement_collector import MeasurementCollector
from slam.data_manager.factory.readers.element_factory import Element
from configs.paths.DEFAULT_FILE_PATHS import KaistDataset

logger = logging.getLogger(__name__)


class KaistReader(DataReader):
    def __init__(self) -> None:
        super().__init__()
        self.__collector = MeasurementCollector(self._dataset_dir)
        self.__iterator = self.__init_iterator()
        self.__sensor_order_file = self._dataset_dir / KaistDataset.data_stamp.value

    def __init_iterator(self) -> None:
        if (DataReader.is_file_valid(self.__sensor_order_file)):
            with open(self.__sensor_order_file, "r") as f:
                names = ["timestamp", "sensor"]
                reader = DictReader(f, fieldnames=names)
                for line in reader:
                    yield line
        else:
            logger.critical(
                f"Couldn't initialize the iterator for {self.__sensor_order_file}")
            sys.exit(1)

    @dispatch
    def get_element(self) -> Element | None:
        try:
            line = next(self.__iterator)
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
        message, location = self.__collector.get_data_by_measurement(line)
        data = message["data"]
        measurement = Measurement(element.measurement.sensor, data)
        element = Element(element.timestamp,
                          measurement,
                          element.location)
        return element

    @dispatch
    def get_element(self, element: dict) -> Element:
        raise NotImplementedError
