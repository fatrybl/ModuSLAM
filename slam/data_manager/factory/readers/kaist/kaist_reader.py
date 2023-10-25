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
from configs.system.data_manager.data_manager import Regime
from configs.system.data_manager.regime import TimeLimit

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
    """Data reader for Kaist Urban Dataset.

    Args:
        DataReader (_type_): Base abstract class.
    """

    EMPTY_STRING: str = ""
    INCORRECT_TIMESTAMP: int = -1
    TIMESTAMP: str = 'timestamp'
    SENSOR_NAME: str = 'sensor_name'

    def __init__(self, dataset_params: Kaist, regime_params: type[Regime]):
        self._dataset_params = dataset_params
        self._regime_params = regime_params
        self._data_stamp_file: Path = dataset_params.directory / \
            dataset_params.paths.data_stamp
        self._collector = MeasurementCollector(
            dataset_params.iterable_data_files,
            dataset_params.data_dirs)
        data_stamp_iterator: Iterator[dict[str, str]] = self.init_iterator()
        self.__current_state = KaistReaderState(
            data_stamp_iterator,
            self._collector.iterators)

        if regime_params.name == TimeLimit.__name__:
            self.__time_range = TimeRange(
                regime_params.start,
                regime_params.stop)
            self._set_initial_state(self.__time_range)

    @property
    def current_state(self) -> KaistReaderState:
        """
        Returns:
            KaistReaderState: state of iterators
        """
        return self.__current_state

    def init_iterator(self) -> Iterator[dict[str, str]]:
        """Initialize a new iterator for a given file. 
            Each line is a dictionary with timestamp and sensor keys.

        Raises:
            FileNotValid: raises when the file does not exist or empty.

        Yields:
            Iterator[dict[str, str]]: file iterator as a dictionary. 
        """
        file = self._data_stamp_file
        if (DataReader._is_file_valid(file)):
            with open(file, "r") as f:
                names = [self.TIMESTAMP, self.SENSOR_NAME]
                reader = DictReader(f, fieldnames=names)
                for line in reader:
                    yield line
        else:
            msg = f"file: {file} is not valid to initialize the iterator"
            logger.critical(msg)
            raise FileNotValid(msg)

    def __reset_current_state(self) -> None:
        """ Re-initializes  all iterators."""

        self._collector.reset_iterators()
        data_stamp_iterator: Iterator[dict[str, str]
                                      ] = self.init_iterator()
        self.__current_state = KaistReaderState(
            data_stamp_iterator,
            self._collector.iterators)

    def __get_file_iterator(self, senor_name: str) -> FileIterator | None:
        """Seeks for the file iterator which corresponds to sensor with the given sensor name.

        Args:
            senor_name (str): name of sensor to look up in the file iterator collection.

        Returns:
            FileIterator | None: for sensor with the given sensor name.
        """
        for it in self.__current_state.sensors_iterators:
            if it.sensor_name == senor_name:
                return it

    def __get_sensor_name(self, timestamp: int) -> tuple[str, int]:
        """Returns the name of the sensor which corresponds to the given timestamp in data_stamp.csv file.
            and a number of iterations before the sensor has been found.

        Args:
            timestamp (int): time of a sensor measurement

        Returns:
            tuple[str, int]: sensor name and number of iterations
        """
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
        """iterates with an iterator until a timestamp is encountered.

        Args:
            it (FileIterator): file iterator
            timestamp (int): timestamp of a measurement.

        Returns:
            int: a number of iterations before the timestamp is encountered.
        """
        current_timestamp: int = self.INCORRECT_TIMESTAMP
        counter: int = 0
        while current_timestamp != timestamp:
            __, line = next(it.iterator)
            current_timestamp = as_int(line[0], logger)
            counter += 1
        return counter

    @dispatch
    def __iterate_N_times(self, N: int, it: FileIterator) -> None:
        """ Overloaded method to iterate N times with the given iterator.

        Args:
            N (int): a number of iterations.
            it (FileIterator): an iterator for a file with sensor timestamps.

        Raises:
            ValueError: amount of iterations is negative.
        """
        if N >= 0:
            for _ in range(N):
                next(it.iterator)
        else:
            msg = f"N must be non-negative, but N = {N}"
            logger.critical(msg)
            raise ValueError(msg)

    @dispatch
    def __iterate_N_times(self, N: int, it: Iterator[dict[str, str]]) -> None:
        """Overloaded method to iterate N times with the given iterator.

        Args:
            N (int): a number of iterations.
            it (Iterator[dict[str, str]]): an iterator for data_stamp.csv file.

        Raises:
            ValueError: amount of iterations is negative.
        """
        if N >= 0:
            for _ in range(N):
                next(it)
        else:
            msg = f"N must be non-negative, but N = {N}"
            logger.critical(msg)
            raise ValueError(msg)

    def _set_initial_state(self, time_range: TimeRange):
        """ Sets the initial state of iterators for Time Range regime.
            1) Gets sensor and N (number of iterations which corresponds to "start" timestamp).
            2) Gets iterator and M (number of iterations for the sensor of "start" timestamp).
            3) Checks if a sensor with the "stop" timestamp has been initialized in SensorFactory
            4) Resers all iterators
            5) Iterates the corresponding iterators N-1 and M-1 times s.t. 
                the future call of next() will return an iterator of the "start" timestamp.

        Args:
            time_range (TimeRange): start and stop timestamps structure.
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
        """
        Gets element from a dataset sequantially based on iterator position. 

        Returns:
            Element | None: element with raw sensor measurement 
                            or None if all measurements from a dataset has already been processed
        """
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
            timestamp = line[self.TIMESTAMP]
            timestamp = as_int(timestamp, logger)
            if self._regime_params.name == TimeLimit.__name__:
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
        """
        Gets an element with raw sensor measurement from a dataset for 
            a given element without raw sensor measurement.

        Args:
            element (Element): without raw sensor measurement.

        Returns:
            Element: with raw sensor measurement.
        """
        sensor: Type[Sensor] = element.measurement.sensor
        timestamp: int = element.timestamp
        message, __ = self._collector.get_data(sensor, timestamp)

        measurement = Measurement(element.measurement.sensor, message.data)
        element = Element(element.timestamp,
                          measurement,
                          element.location)
        return element

    @dispatch
    def get_element(self, sensor: Sensor, timestamp: int | None = None) -> Element:
        """
        Gets an element with raw sensor measurement from a dataset for 
            a given sensor and timestamp. If timestamp is None, 
            gets the element sequantally based on iterator position.

        Args:
            sensor (Sensor): a sensor to get measurement of.
            init_time (int | None, optional): timestamp of sensor`s measurement. 
                                                Defaults to None.

        Returns:
            Element: with raw sensor measurement.
        """
        if timestamp:
            message, location = self._collector.get_data(sensor, timestamp)
        else:
            message, location = self._collector.get_data(sensor)
            timestamp: int = as_int(message.timestamp, logger)

        measurement = Measurement(sensor, message.data)
        element = Element(timestamp,
                          measurement,
                          location)
        return element
