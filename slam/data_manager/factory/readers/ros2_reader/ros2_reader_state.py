import logging
from pathlib import Path

from slam.data_manager.factory.readers.kaist.iterators import FileIterator

logger = logging.getLogger(__name__)


class Ros2ReaderState:
    """
    data_stamp_iterator: iterator for data_stamp.csv file, controlling the order of measurements.
    sensors_iterators: set of iterators for each <SENSOR>_stamp.csv file.
    """

    _EMPTY_STRING: str = ""
    _INCORRECT_TIMESTAMP: int = -1

    def __init__(self, data_stamp_path: Path, sensor_timestamp_file_table: dict[str, Path]):
        self._table = sensor_timestamp_file_table

        self.data_stamp_iterator = FileIterator(data_stamp_path)
        self.sensors_iterators: dict[str, FileIterator] = self._init_table(
            sensor_timestamp_file_table
        )


if __name__ == "__main__":
    from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import (
        Ros2Config,
    )

    print("testing")
    my_path = Path()
    my_config = Ros2Config(directory=my_path)
    data_stamp_file: Path = my_config.directory / my_config.data_stamp_file

    csv_files_table: dict[str, Path] = my_config.csv_files_table
