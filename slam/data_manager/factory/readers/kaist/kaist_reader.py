import logging
from pathlib import Path
from typing import cast, overload

from plum import dispatch

from slam.data_manager.factory.data_reader_ABC import DataReader
from slam.data_manager.factory.element import Element, Measurement
from slam.data_manager.factory.readers.kaist.iterators import FileIterator
from slam.data_manager.factory.readers.kaist.kaist_reader_state import KaistReaderState
from slam.data_manager.factory.readers.kaist.measurement_collector import (
    MeasurementCollector,
)
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import (
    StreamConfig,
    TimeLimitConfig,
)
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.auxiliary_methods import as_int
from slam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(__name__)


class KaistReader(DataReader):
    """Data reader for Kaist Urban Dataset."""

    def __init__(self, dataset_params: KaistConfig, regime_params: TimeLimitConfig | StreamConfig):
        data_stamp_file: Path = dataset_params.directory / dataset_params.data_stamp_file
        csv_files_table: dict[str, Path] = dataset_params.csv_files_table
        lidar_data_dirs_table: dict[str, Path] = dataset_params.lidar_data_dir_table
        stereo_data_dirs_table: dict[str, Path] = dataset_params.stereo_data_dir_table
        self._dataset_directory: Path = dataset_params.directory
        self._regime_name: str = regime_params.name
        self._apply_dataset_dir(
            root_dir=dataset_params.directory,
            tables=(csv_files_table, lidar_data_dirs_table, stereo_data_dirs_table),
        )

        self._collector = MeasurementCollector(lidar_data_dirs_table, stereo_data_dirs_table)

        self._reader_state = KaistReaderState(data_stamp_file, csv_files_table)

        if self._regime_name == TimeLimitConfig.name:
            regime_params = cast(TimeLimitConfig, regime_params)
            self._time_range = TimeRange(regime_params.start, regime_params.stop)
            self._reader_state.init_state(self._time_range)

    @staticmethod
    def _apply_dataset_dir(root_dir: Path, tables: tuple[dict[str, Path], ...]) -> None:
        for table in tables:
            [table.update({sensor_name: root_dir / path}) for sensor_name, path in table.items()]

    @overload
    def get_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """
        try:
            sensor, iterator, t = self._reader_state.next_sensor()

        except StopIteration:
            return None

        timestamp: int = as_int(t)
        if self._regime_name == TimeLimitConfig.name and timestamp > self._time_range.stop:
            return None

        message, location = self._collector.get_data(sensor.name, iterator)
        timestamp_int = as_int(message.timestamp)
        measurement = Measurement(sensor, message.data)
        element = Element(timestamp_int, measurement, location)
        return element

    @overload
    def get_element(self, sensor: Sensor) -> Element | None:
        """
        @overload.
        Gets an element with raw sensor measurement from a dataset for
            a given sensor sequentially based on iterator position.

        Args:
            sensor (Sensor): a sensor to get measurement of.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements of the given sensor has already been processed.
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

        timestamp = as_int(message.timestamp)
        if self._regime_name == TimeLimitConfig.name and timestamp > self._time_range.stop:
            return None

        measurement = Measurement(sensor, message.data)
        element = Element(timestamp, measurement, location)
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

        timestamp: int = as_int(message.timestamp)
        measurement = Measurement(sensor, message.data)
        element_with_data = Element(timestamp, measurement, location)
        return element_with_data

    @overload
    def get_element(self, sensor: Sensor, timestamp: int) -> Element:
        """
        @overload.
        Gets an element with raw sensor measurement from a dataset for
            a given sensor and timestamp. If timestamp is None,
            gets the element sequentially based on iterator position.

        Args:
            sensor (Sensor): a sensor to get measurement of.
            timestamp (int): timestamp of sensor`s measurement.

        Returns:
            Element: with raw sensor measurement with the given timestamp.
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

        timestamp = as_int(message.timestamp)
        measurement = Measurement(sensor, message.data)
        element = Element(timestamp, measurement, location)
        return element

    @dispatch
    def get_element(self, element=None, timestamp=None):
        """Gets element from a dataset in different regimes based on arguments.

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
                                        a given sensor sequentially based on iterator position.
                Returns:
                    Element | None: element with raw sensor measurement
                                    or None if all measurements of the given sensor has already been processed.

            4.
                Args:
                    sensor (Sensor): Gets an element with raw sensor measurement from a dataset for
                                        a given sensor and timestamp. If timestamp is None,
                                        gets the element sequentially based on iterator position.
                    timestamp (int): timestamp of sensor`s measurement.

                Returns:
                    element (Element): with raw sensor measurement of the given timestamp.
        """
