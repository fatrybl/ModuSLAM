import os
from pathlib import Path

from moduslam.data_manager.factory.data_reader_ABC import DataReader
from moduslam.data_manager.factory.element import Element, RawMeasurement

# TODO: Create Rosbags manager to manage Topics, Sensors, Iteration, etc...
from moduslam.data_manager.factory.readers.ros2.rosbags2_manager import Rosbags2Manager

# from moduslam.data_manager.factory.readers.ros2.data_iterator import Iterator
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)  # TODO: Change the configuration file to ROS2Config
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from moduslam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from moduslam.utils.auxiliary_dataclasses import TimeRange


class Ros2DataReader(DataReader):
    """Data reader for ROS2 in test."""

    def __init__(self, regime: TimeLimit | Stream, dataset_params: Ros2Config):
        self._dataset_directory: Path = dataset_params.directory
        self._regime = regime
        self.sensors_table = dataset_params.sensors_table

        if isinstance(self._regime, TimeLimit):
            self._time_range = TimeRange(self._regime.start, self._regime.stop)
            self.rosbags_manager = Rosbags2Manager(
                self._dataset_directory, self.sensors_table, self._time_range
            )

        else:
            self.rosbags_manager = Rosbags2Manager(self._dataset_directory, self.sensors_table)

        # for i in range(10):
        #     element = self.get_element()
        #     if element is not None:
        #         print(f"Got element: {element}")

    def get_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """

        sensor_id, location, message, t = self.rosbags_manager.next_sensor_read()
        print(f"Got sensor: {sensor_id}")
        for sensor in self.rosbags_manager.sensors_list:
            if sensor["id"] == sensor_id:
                sensor_name = sensor["sensor_type"]
                print(f"That means sensor {sensor_name}")
                break
        try:
            sensor = SensorsFactory.get_sensor(sensor_name)

        # except StopIteration:
        except Exception as e:
            print(f"Failed to get sensor {sensor_name} with error message: {e}")
            return None

        # timestamp: int = as_int(t)
        if isinstance(self._regime, TimeLimit) and t > self._time_range.stop:
            return None

        measurement = RawMeasurement(sensor, message)
        element = Element(t, measurement, location)

        return element


if __name__ == "__main__":

    print("Testing ROS2 data reader")
    folder_path = Path(os.environ["DATA_DIR"])
    print(folder_path)
    bag_path = Path("{}/rosbag2_2024_1713944720".format(folder_path))

    timelimit1 = TimeLimit(start=10, stop=20)
    timelimit2 = Stream()
    ros2_config = Ros2Config(directory=bag_path)

    reader = Ros2DataReader(regime=timelimit1, dataset_params=ros2_config)

    my_config = SensorFactoryConfig()
    SensorsFactory.init_sensors(config=my_config)

    reader.get_element()
