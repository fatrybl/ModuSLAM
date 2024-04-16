from pathlib import Path

from slam.data_manager.factory.data_reader_ABC import DataReader
from slam.data_manager.factory.element import Element
from slam.data_manager.factory.readers.ros2_reader.ros2_reader_state import Ros2ReaderState
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import Ros2Config
from slam.system_configs.system.data_manager.batch_factory.regime import (
    Stream,
    TimeLimit,
)


class Ros2DataReader(DataReader):
    """Data reader for ROS2 in test."""

    def __init__(self, regime: TimeLimit | Stream, dataset_params: Ros2Config):
        data_stamp_file: Path = dataset_params.directory / dataset_params.data_stamp_file
        csv_files_table: dict[str, Path] = dataset_params.csv_files_table
        lidar_data_dirs_table: dict[str, Path] = dataset_params.lidar_data_dir_table
        stereo_data_dirs_table: dict[str, Path] = dataset_params.stereo_data_dir_table
        self._dataset_directory: Path = dataset_params.directory
        self._regime = regime

        self._reader_state = Ros2ReaderState(data_stamp_file, csv_files_table)

        self._apply_dataset_dir(
            root_dir=dataset_params.directory,
            tables=(csv_files_table, lidar_data_dirs_table, stereo_data_dirs_table),
        )

    @staticmethod
    def _apply_dataset_dir(root_dir: Path, tables: tuple[dict[str, Path], ...]) -> None:
        for table in tables:
            [table.update({sensor_name: root_dir / path}) for sensor_name, path in table.items()]


    def get_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed

        try:
            sensor, iterator, t = self._reader_state.next_sensor()

        except StopIteration:
            return None

        timestamp: int = as_int(t)
        if isinstance(self._regime, TimeLimit) and timestamp > self._time_range.stop:
            return None

        message, location = self._collector.get_data(sensor.name, iterator)
        timestamp_int = as_int(message.timestamp)
        measurement = Measurement(sensor, message.data)
        element = Element(timestamp_int, measurement, location)
        return element
        """

        try:
            sensor, iterator, t = self._reader_state.next_sensor()

        except:
            print("Could not read the data")