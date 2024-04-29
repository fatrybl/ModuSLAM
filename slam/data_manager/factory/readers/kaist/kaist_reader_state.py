import logging
from collections import Counter
from pathlib import Path

from slam.data_manager.factory.readers.kaist.iterators import FileIterator
from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.auxiliary_methods import as_int
from slam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(__name__)


class KaistReaderState:
    """State of iterators for KAIST data reader.

    Attributes:
        data_stamp_iterator: iterator for data_stamp.csv file, controlling the order of measurements.
        sensors_iterators: iterators for each <SENSOR>_stamp.csv file.
    """

    _EMPTY_STRING: str = ""
    _INCORRECT_TIMESTAMP: int = -1

    def __init__(self, data_stamp_path: Path, sensor_timestamp_file_table: dict[str, Path]):
        """
        Args:
            data_stamp_path: path to data_stamp.csv file.
            sensor_timestamp_file_table: table of "sensor -> timestamp file" pairs.
        """

        self._table = sensor_timestamp_file_table

        self.data_stamp_iterator = FileIterator(data_stamp_path)
        self.sensors_iterators: dict[str, FileIterator] = self._init_table(
            sensor_timestamp_file_table
        )

    def next_sensor(self) -> tuple[Sensor, FileIterator, str]:
        """Gets the next sensor, its iterator and the timestamp.

        Raises:
            StopIteration: all data has been processed.
        """
        while True:
            try:
                line = next(self.data_stamp_iterator)
            except StopIteration:
                msg = f"All data in {self.data_stamp_iterator.file.name!r} has been processed."
                logger.info(msg)
                raise

            timestamp: str = line[0]
            sensor_name: str = line[1]
            try:
                sensor: Sensor = SensorsFactory.get_sensor(sensor_name)
            except ItemNotFoundError:
                logger.warning(f"Sensor {sensor_name!r} has not been found.")
                continue

            iterator = self.sensors_iterators[sensor.name]
            return sensor, iterator, timestamp

    def init_state(self, time_range: TimeRange) -> None:
        """Initializes the state of iterators for Time Range regime.

        Args:
            time_range: start & stop timestamps.
        """
        start: int = time_range.start

        first_sensor_name, occurrences = self._get_sensor_and_occurrences(start)
        self.reset()

        for sensor_name, num_occurrences in occurrences.items():
            iterator = self.sensors_iterators[sensor_name]
            if sensor_name == first_sensor_name:
                num_iterations = num_occurrences - 1
            else:
                num_iterations = num_occurrences

            self._iterate_n_times(num_iterations, iterator)

        n: int = sum(occurrences.values())
        self._iterate_n_times(n - 1, self.data_stamp_iterator)

    def reset(self) -> None:
        """Resets all iterators to the initial position."""
        self.data_stamp_iterator = FileIterator(self.data_stamp_iterator.file)
        self.sensors_iterators = self._init_table(self._table)

    @staticmethod
    def _init_table(sensor_timestamp_file_table: dict[str, Path]) -> dict[str, FileIterator]:
        """Initializes the "sensor_name -> file iterator" table.

        Args:
            sensor_timestamp_file_table: table of sensors` timestamp files.

        Returns:
            table of iterators for each sensor`s timestamp file.
        """
        table = {}
        for sensor_name, file_path in sensor_timestamp_file_table.items():
            table[sensor_name] = FileIterator(file_path)
        return table

    @staticmethod
    def _iterate_n_times(n: int, iterator: FileIterator) -> None:
        """Iterates N times over the given iterator.

        Args:
            n: a number of iterations.

            iterator: an iterator for a file with sensor timestamps.

        Raises:
            ValueError: amount of iterations is negative.
            StopIteration: can not iterate N times for the given file iterator.
        """
        if n < 0:
            msg = f"Incorrect number of iterations: {n}"
            logger.critical(msg)
            raise ValueError(msg)

        for _ in range(n):
            try:
                next(iterator)
            except StopIteration:
                msg = f"Can not iterate N={n} times for file: {iterator.file!r}"
                logger.critical(msg)
                raise

    def _get_sensor_and_occurrences(self, timestamp: int) -> tuple[str, Counter]:
        """Returns the name of the sensor which corresponds to the given timestamp in
        data_stamp.csv file and a number of occurrences of each sensor before the given
        timestamp.

        Args:
            timestamp: time of the sensor`s measurement.

        Returns:
            sensor name and number of occurrences of each sensor before the given timestamp.

        Raises:
            StopIteration: can not find a line with the given timestamp in data_stamp.csv file.
        """
        current_timestamp: int = self._INCORRECT_TIMESTAMP
        sensor_name: str = self._EMPTY_STRING
        occurrence: Counter = Counter()

        while current_timestamp != timestamp:
            try:
                line = next(self.data_stamp_iterator)
            except StopIteration:
                msg = f"Can not find a line with timestamp {timestamp} in {self.data_stamp_iterator.file!r}"
                logger.critical(msg)
                raise
            else:
                t: str = line[0]
                sensor_name = line[1]
                current_timestamp = as_int(t)
                occurrence.update({sensor_name})

        return sensor_name, occurrence
