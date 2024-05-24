import logging
from pathlib import Path
from typing import overload

from plum import dispatch

from moduslam.data_manager.factory.data_reader_ABC import DataReader
from moduslam.data_manager.factory.element import Element, RawMeasurement
from moduslam.data_manager.factory.readers.kaist.iterators import FileIterator
from moduslam.data_manager.factory.readers.kaist.kaist_reader_state import (
    KaistReaderState,
)
from moduslam.data_manager.factory.readers.kaist.measurement_collector import (
    MeasurementCollector,
)
from moduslam.logger.logging_config import data_manager
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_methods import to_int
from moduslam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(data_manager)


class KaistReader(DataReader):
    """Data reader for Kaist Urban Dataset."""

    def __init__(self, regime: TimeLimit | Stream, dataset_params: KaistConfig):
        data_stamp_file: Path = dataset_params.directory / dataset_params.data_stamp_file
        csv_files_table: dict[str, Path] = dataset_params.csv_files_table
        lidar_data_dirs_table: dict[str, Path] = dataset_params.lidar_data_dir_table
        stereo_data_dirs_table: dict[str, Path] = dataset_params.stereo_data_dir_table
        self._dataset_directory: Path = dataset_params.directory
        self._regime = regime

        self._apply_dataset_dir(
            root_dir=dataset_params.directory,
            tables=(csv_files_table, lidar_data_dirs_table, stereo_data_dirs_table),
        )

        self._collector = MeasurementCollector(lidar_data_dirs_table, stereo_data_dirs_table)

        self._reader_state = KaistReaderState(data_stamp_file, csv_files_table)

        if isinstance(self._regime, TimeLimit):
            self._time_range = TimeRange(self._regime.start, self._regime.stop)
            self._reader_state.init_state(self._time_range)

    @overload
    def get_element(self) -> Element | None:
        """
        @overload.

        Gets element from a dataset sequentially based on iterator position.

        Returns:
            element with raw measurement or None if all measurements from a dataset has already been processed.
        """
        try:
            sensor, iterator, t = self._reader_state.next_sensor()

        except StopIteration:
            return None

        timestamp: int = to_int(t)
        if isinstance(self._regime, TimeLimit) and timestamp > self._time_range.stop:
            return None

        message, location = self._collector.get_data(sensor.name, iterator)
        timestamp_int = to_int(message.timestamp)
        measurement = RawMeasurement(sensor, message.data)
        element = Element(timestamp_int, measurement, location)
        return element

    @overload
    def get_element(self, sensor: Sensor) -> Element | None:
        """
        @overload.

        Gets element from a dataset sequentially based on iterator position for the specific sensor.

        Args:
            sensor: a sensor to get measurement of.

        Returns:
            element with raw measurement or None if all measurements from a dataset has already been processed.
        """
        try:
            iterator: FileIterator = self._reader_state.sensors_iterators[sensor.name]
        except KeyError:
            msg = f"Sensor {sensor.name!r} is not in the dataset."
            logger.error(msg)
            return None

        try:
            message, location = self._collector.get_data(sensor.name, iterator)
        except StopIteration:
            return None

        timestamp = to_int(message.timestamp)
        if isinstance(self._regime, TimeLimit) and timestamp > self._time_range.stop:
            return None

        measurement = RawMeasurement(sensor, message.data)
        element = Element(timestamp, measurement, location)
        return element

    @overload
    def get_element(self, element: Element) -> Element:
        """
        @overload.

        Gets the element with raw measurement from a dataset for the given element without raw measurement.

        Args:
            element (Element): without raw measurement.

        Returns:
            element with raw measurement.

        Raises:
            ItemNotFoundError: the given element is not in the dataset.
        """

        sensor: Sensor = element.measurement.sensor
        try:
            iterator: FileIterator = self._reader_state.sensors_iterators[sensor.name]
        except KeyError:
            msg = f"Incorrect input element: no sensor {sensor.name!r} in the dataset."
            logger.error(msg)
            raise ItemNotFoundError(msg)

        iterator.reset()  # init fresh iterator

        try:
            message, location = self._collector.get_data(sensor.name, iterator, element.timestamp)
        except ItemNotFoundError:
            msg = (
                f"Incorrect input element: no measurement found for the sensor {sensor.name!r} "
                f"and the timestamp {element.timestamp}."
            )
            logger.error(msg)
            raise ItemNotFoundError(msg)

        timestamp: int = to_int(message.timestamp)
        measurement = RawMeasurement(sensor, message.data)
        element_with_data = Element(timestamp, measurement, location)
        return element_with_data

    @overload
    def get_element(self, sensor: Sensor, timestamp: int) -> Element:
        """
        @overload.

        Gets an element with raw sensor measurement from a dataset for the given sensor and timestamp.

        Args:
            sensor (Sensor): a sensor to get measurement of.

            timestamp (int): timestamp of sensor`s measurement.

        Returns:
            element with raw measurement.

        Raises:
            ItemNotFoundError: the element of the given sensor and timestamp is not in the dataset.
        """

        try:
            iterator: FileIterator = self._reader_state.sensors_iterators[sensor.name]
        except KeyError:
            msg = f"Incorrect input element: no sensor {sensor.name!r} in the dataset."
            logger.error(msg)
            raise ItemNotFoundError(msg)

        iterator.reset()  # init fresh iterator not to slip the required measurement.

        try:
            message, location = self._collector.get_data(sensor.name, iterator, timestamp)
        except ItemNotFoundError:
            msg = (
                f"Incorrect input element: no measurement found for the sensor {sensor.name!r} "
                f"and the timestamp {timestamp}."
            )
            logger.error(msg)
            raise ItemNotFoundError(msg)

        timestamp = to_int(message.timestamp)
        measurement = RawMeasurement(sensor, message.data)
        element = Element(timestamp, measurement, location)
        return element

    @dispatch
    def get_element(self, element=None, timestamp=None):
        """
        @overload.

        Gets element from a dataset in different regimes based on arguments.

        Calls:
            1.  Gets element from a dataset sequentially based on iterator position for the specific sensor.

                Args:
                    __.

                Returns:
                    element (Element) with raw measurement or None if all measurements from a dataset
                     has already been processed.

            2.  Gets the element with raw measurement from a dataset for the given element without raw measurement.

                Args:
                    sensor (Sensor): sensor to get measurement of.

                Returns:
                    element (Element) with raw measurement.

            3.  Gets the element with raw measurement from a dataset for the given element without raw measurement.

                Args:
                    element (Element): without raw measurement.

                Returns:
                    element with raw measurement.

                Raises:
                    ItemNotFoundError: the given element is not in the dataset.

            4.  Gets an element with raw sensor measurement from a dataset for the given sensor and timestamp.

                Args:
                    sensor (Sensor): sensor to get measurement of.

                    timestamp (int): timestamp of sensor`s measurement.

                Returns:
                    element (Element) with raw measurement.

                Raises:
                    ItemNotFoundError: the element of the given sensor and timestamp is not in the dataset.
        """

    @staticmethod
    def _apply_dataset_dir(root_dir: Path, tables: tuple[dict[str, Path], ...]) -> None:
        """Updates the paths in the tables with the root directory.

        Args:
            root_dir: root directory to be added to the paths in the tables.
            tables: tables with the paths to be updated.
        """
        for table in tables:
            [table.update({sensor_name: root_dir / path}) for sensor_name, path in table.items()]
