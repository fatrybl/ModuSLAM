import logging
from collections import Counter
from collections.abc import Iterator
from csv import DictReader
from dataclasses import dataclass
from pathlib import Path
from typing import cast, overload

from plum import dispatch

from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig
from configs.system.data_manager.batch_factory.regime import (
    RegimeConfig,
    TimeLimitConfig,
)
from slam.data_manager.factory.readers.data_reader_ABC import DataFlowState, DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.kaist.measurement_collector import (
    FileIterator,
    MeasurementCollector,
)
from slam.setup_manager.sensor_factory.factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.auxiliary_methods import as_int
from slam.utils.exceptions import FileNotValid, SensorNotFound

logger = logging.getLogger(__name__)


@dataclass
class KaistReaderState(DataFlowState):
    """
    data_stamp_iterator: iterator for data_stamp.csv file, controling the order of measurements.
    sensors_iterators: set of iterators for each <SENSOR>_stamp.csv file.
    """

    data_stamp_iterator: Iterator[dict[str, str]]
    sensors_iterators: set[FileIterator]


class CsvFileGenerator:
    """
    Generator for a file to read each row of "data_stamp.csv" as a dictionary.
    """

    def __init__(self, file_path: Path, names: list[str]):
        """
        Args:
            file_path (Path): file to read.
            names (list[str]): dictionary keys` names.
        """
        self.__file = open(file_path, "r")
        self.__reader = DictReader(self.__file, fieldnames=names)

    def __next__(self) -> dict[str, str]:
        try:
            val = next(self.__reader)
            return val
        except StopIteration:
            self.__file.close()
            raise

    def __iter__(self):
        return self


class KaistReader(DataReader):
    """
    Data reader for Kaist Urban Dataset.

    TODO: Synchronize sensors` iterators for data_stamp.csv and <SENSOR>_stamp.csv:
    TODO: check if a timestamp from data_stamp.csv exists in  <SENSOR>_stamp.csv
    """

    __EMPTY_STRING: str = ""
    __INCORRECT_TIMESTAMP: int = -1
    __TIMESTAMP: str = "timestamp"
    __SENSOR_NAME: str = "sensor_name"

    def __init__(self, dataset_params: KaistConfig, regime_params: RegimeConfig):
        """
        TODO: add better regime_params type validation.
        """
        self._dataset_params = dataset_params
        self._regime_params = regime_params
        self._data_stamp_file: Path = dataset_params.directory / dataset_params.paths.data_stamp
        self._collector = MeasurementCollector(dataset_params.iterable_data_files, dataset_params.data_dirs)
        data_stamp_iterator: Iterator[dict[str, str]] = self._init_iterator()
        self.__current_state = KaistReaderState(data_stamp_iterator, self._collector.iterators)

        if regime_params.name == TimeLimitConfig.name:
            regime_params = cast(TimeLimitConfig, regime_params)
            self.__time_range = TimeRange(regime_params.start, regime_params.stop)
            self._set_initial_state(self.__time_range)

    @property
    def current_state(self) -> KaistReaderState:
        """
        Returns:
            KaistReaderState: state of iterators
        """
        return self.__current_state

    def _init_iterator(self) -> Iterator[dict[str, str]]:
        """
        Initialize a new iterator for a given file.
            Each line is a dictionary with timestamp and sensor keys.

        Raises:
            FileNotValid: raises when the file does not exist or empty.

        Yields:
            Iterator[dict[str, str]]: file iterator as a dictionary.
        """
        file = self._data_stamp_file
        if DataReader.is_file_valid(file):
            names: list[str] = [self.__TIMESTAMP, self.__SENSOR_NAME]
            return CsvFileGenerator(file, names)
        else:
            msg = f"file: {file} is not valid to initialize the iterator"
            logger.critical(msg)
            raise FileNotValid(msg)

    def __reset_current_state(self) -> None:
        """
        Re-initializes all iterators.
        """

        self._collector.reset_iterators()
        data_stamp_iterator: Iterator[dict[str, str]] = self._init_iterator()
        self.__current_state = KaistReaderState(data_stamp_iterator, self._collector.iterators)

    def __get_file_iterator(self, senor_name: str) -> FileIterator | None:
        """
        Seeks for the file iterator which corresponds to sensor with the given sensor name.

        Args:
            senor_name (str): name of sensor to look up in the file iterator collection.

        Returns:
            FileIterator | None: iterator for sensor with the given sensor name.
        """
        iterator: FileIterator | None = None
        for it in self.__current_state.sensors_iterators:
            if it.sensor_name == senor_name:
                iterator = it
                break
        return iterator

    def __get_sensor_name(self, timestamp: int) -> tuple[str, Counter]:
        """
        Returns the name of the sensor which corresponds to the given timestamp
        in data_stamp.csv file and a number of occurrences of each sensor before the given timestamp.

        Args:
            timestamp (int): time of a sensor measurement

        Returns:
            tuple[str, Counter]:
                sensor name and number of occurrences of each sensor before the given timestamp.
        """
        current_timestamp: int = self.__INCORRECT_TIMESTAMP
        sensor_name: str = self.__EMPTY_STRING
        occurrence: Counter = Counter()

        while current_timestamp != timestamp:
            try:
                current_line = next(self.__current_state.data_stamp_iterator)
            except StopIteration:
                msg = f"can not find a line with timestamp {timestamp} in {self._data_stamp_file}"
                logger.critical(msg)
                raise
            else:
                current_timestamp = as_int(current_line[self.__TIMESTAMP])
                sensor_name = current_line[self.__SENSOR_NAME]
                occurrence.update({sensor_name})

        return sensor_name, occurrence

    @overload
    def __iterate_n_times(self, n: int, it: FileIterator) -> None:
        """
        @overload.
        Overloaded method to iterate N times with the given iterator.

        Args:
            n (int): a number of iterations.
            it (FileIterator): an iterator for a file with sensor timestamps.

        Raises:
            ValueError: amount of iterations is negative.
        """
        if n >= 0:
            for _ in range(n):
                try:
                    next(it.iterator)
                except StopIteration:
                    msg = f"can not iterate N={n} times for file: {it.file}"
                    logger.critical(msg)
                    raise
        else:
            msg = f"N must be non-negative, but N = {n}"
            logger.critical(msg)
            raise ValueError(msg)

    @overload
    def __iterate_n_times(self, n: int, it: Iterator[dict[str, str]]) -> None:
        """
        @overload.
        Overloaded method to iterate N times with the given iterator.

        Args:
            n (int): a number of iterations.
            it (Iterator[dict[str, str]]): an iterator for data_stamp.csv file.

        Raises:
            ValueError: amount of iterations is negative.
        """
        if n >= 0:
            for _ in range(n):
                try:
                    next(it)
                except StopIteration:
                    msg = f"can not iterate N={n} times with iterator: {it}"
                    logger.critical(msg)
                    raise
        else:
            msg = f"N must be non-negative, but N = {n}"
            logger.critical(msg)
            raise ValueError(msg)

    @dispatch
    def __iterate_n_times(self, n=None, it=None):
        """
        @overload.

        Iterates N times with the given iterator.

        Calls:
            1.  Args:
                    n (int): a number of iterations.
                    it (FileIterator): an iterator for a file with sensor timestamps.
            2.  Args:
                    n (int): a number of iterations.
                    it (Iterator[dict[str, str]]): an iterator for data_stamp.csv file.
        """

    def _set_initial_state(self, time_range: TimeRange):
        """
        Sets the initial state of iterators for Time Range regime.
            1) Gets sensor`s name and N - number of occurrences of each sensor
                before the given "start" timestamp.
            2) Resets all iterators for the future search.
            3) Gets sensor`s name which corresponds to "stop" timestamp.
            4) Сhecks if start/stop sensors are initialized in SensorFactory Singleton.
            5) Resets all iterators for the future search.
            6) Sets all iterators to the "pre-start" position s.t.
                the future call of next() will return values of the "start" position (timestamp).

        Args:
            time_range (TimeRange): start & stop timestamps structure.
        """

        first_sensor_name, occurrences = self.__get_sensor_name(time_range.start)
        self.__reset_current_state()
        last_sensor_name, __ = self.__get_sensor_name(time_range.stop)
        first_sensor: Sensor = SensorFactory.get_sensor(first_sensor_name)
        last_sensor: Sensor = SensorFactory.get_sensor(last_sensor_name)
        used_sensors = SensorFactory.get_used_sensors()
        for sensor in [first_sensor, last_sensor]:
            if sensor not in used_sensors:
                msg = f"sensor {sensor} is not in used_sensors {used_sensors}"
                logger.critical(msg)
                raise SensorNotFound(msg)

        self.__reset_current_state()

        for item in occurrences:
            sensor_name = item
            count = occurrences[item]
            iterator = self.__get_file_iterator(sensor_name)
            if iterator is None:
                msg = f"iterator for sensor {sensor_name} has not been found"
                logger.critical(msg)
                raise ValueError(msg)
            if sensor_name == first_sensor_name:
                self.__iterate_n_times(count - 1, iterator)
            else:
                self.__iterate_n_times(count, iterator)

        n: int = sum(occurrences.values())
        self.__iterate_n_times(n - 1, self.__current_state.data_stamp_iterator)

    @overload
    def get_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """
        used_sensors = SensorFactory.get_used_sensors()
        try:
            while True:
                line = next(self.__current_state.data_stamp_iterator)
                sensor = SensorFactory.get_sensor(line[self.__SENSOR_NAME])
                if sensor in used_sensors:
                    break

        except StopIteration:
            msg = f"{self.__current_state.data_stamp_iterator} has been processed"
            logger.debug(msg)
            return None

        else:
            if self._regime_params.name == TimeLimitConfig.name:
                timestamp: str = line[self.__TIMESTAMP]
                timestamp_int: int = as_int(timestamp)
                if timestamp_int > self.__time_range.stop:
                    return None

            message, location = self._collector.get_data(sensor)
            timestamp_int = as_int(message.timestamp)
            measurement = Measurement(sensor, message.data)
            element = Element(timestamp_int, measurement, location)
            return element

    @overload
    def get_element(self, element: Element) -> Element:
        """
        @overload.
        Gets an element with raw sensor measurement from a dataset for
            a given element without raw sensor measurement.

        Args:
            element (Element): without raw sensor measurement.

        Returns:
            Element: with raw sensor measurement.
        """
        sensor: Sensor = element.measurement.sensor
        message, location = self._collector.get_data(sensor, element.timestamp)

        timestamp: int = as_int(message.timestamp)
        measurement = Measurement(sensor, message.data)
        element = Element(timestamp, measurement, location)
        return element

    @overload
    def get_element(self, sensor: Sensor, timestamp: int | None = None) -> Element:
        """
        @overload.
        Gets an element with raw sensor measurement from a dataset for
            a given sensor and timestamp. If timestamp is None,
            gets the element sequantally based on iterator position.

        Args:
            sensor (Sensor): a sensor to get measurement of.
            timestamp (int | None, optional): timestamp of sensor`s measurement.
                                                Defaults to None.

        Returns:
            Element: with raw sensor measurement.
        """

        if timestamp:
            message, location = self._collector.get_data(sensor, timestamp)
        else:
            message, location = self._collector.get_data(sensor)
            timestamp = as_int(message.timestamp)

        measurement = Measurement(sensor, message.data)
        element = Element(timestamp, measurement, location)
        return element

    @dispatch
    def get_element(self, element=None, timestamp=None):
        """
        Gets element from a dataset in different regimes based on arguments.

        Calls:
            1.
                Args:
                    __: Gets element from a dataset sequentially based on iterator position.

                Returns:
                    Element | None: element with raw sensor measurement
                                    or None if all measurements from a dataset has already been processed.
            2.
                Args:
                    element (Element): Gets an element with raw sensor measurement from a dataset for
                                        a given element without raw sensor measurement.

                Returns:
                    element (Element): with raw sensor measurement.
            3.
                Args:
                    sensor (Sensor): Gets an element with raw sensor measurement from a dataset for
                                        a given sensor and timestamp. If timestamp is None,
                                        gets the element sequentially based on iterator position.
                    timestamp (int | None): timestamp of sensor`s measurement. Defaults to None.

                Returns:
                    element (Element): with raw sensor measurement.
        """
