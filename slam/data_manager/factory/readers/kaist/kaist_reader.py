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
    MeasurementCollector, FileIterator)
from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.exceptions import FileNotValid, SensorNotFound
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor
from slam.utils.auxiliary_methods import as_int

from configs.system.data_manager.datasets.kaist import Kaist
from configs.system.data_manager.manager import TimeRange as TimeRangeRegime
from configs.system.data_manager.manager import Regime

logger = logging.getLogger(__name__)


@dataclass
class KaistReaderState(DataFlowState):
    """
    data_stam_iterator: iterator for data_stamp.csv file, controling the order of measurements.
    sensors_iterators: set of iterators for each <SENSOR>_stamp.csv file. 
    """
    data_stamp_iterator: Iterator[dict[str, str]]
    sensors_iterators: set[FileIterator]


class KaistReader(DataReader):
    EMPTY_STRING: str = ""
    INCORRECT_TIMESTAMP: int = -1
    TIMESTAMP: str = 'timestamp'
    SENSOR_NAME: str = 'sensor_name'

    def __init__(self, dataset_params: Kaist, regime_params: type[Regime]):
        self._dataset_params = dataset_params
        self._regime_params = regime_params
        self._collector = MeasurementCollector(
            dataset_params.iterable_data_files, dataset_params.data_dirs)
        data_stamp_iterator: Iterator[dict[str, str]] = self.init_iterator(
            dataset_params.data_stamp_file)
        self.__current_state = KaistReaderState(
            data_stamp_iterator,
            self._collector.iterators)

        if regime_params.name == TimeRangeRegime.__name__:
            self.__time_range = TimeRange(
                regime_params.start,
                regime_params.stop)
            self._set_initial_state(self.__time_range)

    @property
    def current_state(self) -> KaistReaderState:
        return self.__current_state

    @classmethod
    def init_iterator(cls, file: Path) -> Iterator[dict[str, str]]:
        if (DataReader._is_file_valid(file)):
            with open(file, "r") as f:
                names = [cls.TIMESTAMP, cls.SENSOR_NAME]
                reader = DictReader(f, fieldnames=names)
                for line in reader:
                    yield line
        else:
            msg = f"file: {file} is not valid to initialize the iterator"
            logger.critical(msg)
            raise FileNotValid(msg)

    def __reset_current_state(self) -> None:
        self._collector.reset_iterators()
        data_stamp_file: Path = self._dataset_params.data_stamp_file
        data_stamp_iterator: Iterator[dict[str, str]
                                      ] = self.init_iterator(data_stamp_file)
        self.__current_state = KaistReaderState(
            data_stamp_iterator,
            self._collector.iterators)

    def __get_file_iterator(self, senor_name: str) -> FileIterator | None:
        for it in self.__current_state.sensors_iterators:
            if it.sensor_name == senor_name:
                return it

    def __get_sensor_name(self, timestamp: int) -> tuple[str, int]:
        current_timestamp: int = self.INCORRECT_TIMESTAMP
        sensor_name: str = self.EMPTY_STRING
        counter: int = 0

        while current_timestamp != timestamp:
            current_line = next(self.__current_state.data_stamp_iterator)
            current_timestamp: int = as_int(
                current_line[self.TIMESTAMP], logger)
            sensor_name = current_line[self.SENSOR_NAME]
            counter += 1

        return sensor_name, counter

    def __iterate_to_timestamp(self, it: FileIterator, timestamp: int) -> int:
        current_timestamp: int = self.INCORRECT_TIMESTAMP
        counter: int = 0
        while current_timestamp != timestamp:
            __, line = next(it.iterator)
            current_timestamp = as_int(line[0], logger)
            counter += 1
        return counter

    @dispatch
    def __iterate_N_times(self, N: int, it: FileIterator) -> None:
        if N >= 0:
            for _ in range(N):
                next(it.iterator)
        else:
            msg = f"N must be non-negative, but N = {N}"
            logger.critical(msg)
            raise ValueError(msg)

    @dispatch
    def __iterate_N_times(self, N: int, it: Iterator[dict[str, str]]) -> None:
        if N >= 0:
            for _ in range(N):
                next(it)
        else:
            msg = f"N must be non-negative, but N = {N}"
            logger.critical(msg)
            raise ValueError(msg)

    def _set_initial_state(self, time_range: TimeRange):
        """ Sets the initial state of the iterators

        Args:
            initial_state (int): timestamp of the first measurement
        """
        first_sensor_name, data_stamp_num_iterations = self.__get_sensor_name(
            time_range.start)
        last_sensor_name, __ = self.__get_sensor_name(
            time_range.stop)
        first_sensor: Type[Sensor] = SensorFactory.name_to_sensor(
            first_sensor_name)
        last_sensor: Type[Sensor] = SensorFactory.name_to_sensor(
            last_sensor_name)

        for sensor in [first_sensor, last_sensor]:
            if sensor not in SensorFactory.used_sensors:
                msg = f"sensor {sensor} is not in used_sensors {SensorFactory.used_sensors}"
                logger.critical(msg)
                raise SensorNotFound(msg)

        sensor_iterator = self.__get_file_iterator(first_sensor.name)
        sensor_stamp_num_iterations = self.__iterate_to_timestamp(
            sensor_iterator, time_range.start)

        self.__reset_current_state()
        self.__iterate_N_times(data_stamp_num_iterations - 1,
                               self.__current_state.data_stamp_iterator)
        self.__iterate_N_times(sensor_stamp_num_iterations - 1,
                               sensor_iterator)

    @dispatch
    def get_element(self) -> Element | None:
        try:
            while True:
                line = next(self.__current_state.data_stamp_iterator)
                sensor = SensorFactory.name_to_sensor(
                    line[self.SENSOR_NAME])
                if sensor in SensorFactory.used_sensors:
                    break

        except StopIteration:
            msg = f"{self.__current_state.data_stamp_iterator} has been processed"
            logger.debug(msg)
            return None

        else:
            sensor: Type[Sensor] = SensorFactory.name_to_sensor(
                line[self.SENSOR_NAME])
            timestamp = line[self.TIMESTAMP]
            timestamp = as_int(timestamp, logger)
            if self._regime_params.name == TimeRangeRegime.__name__:
                if timestamp > self.__time_range.stop:
                    return None

            self._collector.iterators = self.__current_state.sensors_iterators
            message, location = self._collector.get_data(sensor)

            measurement = Measurement(sensor, message.data)
            element = Element(timestamp,
                              measurement,
                              location)
            return element

    @dispatch
    def get_element(self, element: Element) -> Element:
        sensor: Type[Sensor] = element.measurement.sensor
        timestamp: int = element.timestamp
        message, __ = self._collector.get_data(sensor, timestamp)

        measurement = Measurement(element.measurement.sensor, message.data)
        element = Element(element.timestamp,
                          measurement,
                          element.location)
        return element

    @dispatch
    def get_element(self, sensor: Sensor, init_time: int | None = None) -> Element:
        if init_time:
            message, location = self._collector.get_data(sensor, init_time)
        else:
            message, location = self._collector.get_data(sensor)

        measurement = Measurement(sensor, message.data)
        timestamp: int = as_int(message.timestamp, logger)
        element = Element(timestamp,
                          measurement,
                          location)
        return element
