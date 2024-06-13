import os
from pathlib import Path

from slam.data_manager.factory.element import Element, RawMeasurement
from slam.data_manager.factory.readers.ros2_reader.data_iterator import Iterator
from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    Ros2Config,
)
from slam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from slam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from slam.utils.auxiliary_dataclasses import TimeRange


class Ros2DataReader():
    """Data reader for ROS2 in test."""

    def __init__(self, regime: TimeLimit | Stream, dataset_params: Ros2Config):
        self._dataset_directory: Path = dataset_params.directory
        self._regime = regime
        self.iterator = Iterator(bagpath=self._dataset_directory)

        if isinstance(self._regime, TimeLimit):
            self._time_range = TimeRange(self._regime.start, self._regime.stop)


    def get_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """

        try:
            sensor, t, iterator = self.iterator.next()

        except StopIteration:

            return None

        # timestamp: int = as_int(t)
        if isinstance(self._regime, TimeLimit) and t > self._time_range.stop:
            return None

        message, location = (sensor[-1], iterator)
        measurement = RawMeasurement(sensor, message.data)
        element = Element(t, measurement, location)

        return element


if __name__ == "__main__":

    print("Testing ROS2 data reader")
    folder_path = Path(os.environ["DATA_DIR"])
    bag_path = Path("{}/rosbag2_2024_1713944720".format(folder_path))

    timelimit1 = TimeLimit(start=10, stop=20)
    timelimit2 = Stream()
    ros2_config = Ros2Config(directory=bag_path)

    reader = Ros2DataReader(regime=timelimit1, dataset_params=ros2_config)

    my_config = SensorFactoryConfig()
    SensorsFactory.init_sensors(config=my_config)

    reader.get_element()
