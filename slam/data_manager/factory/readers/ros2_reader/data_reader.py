import os
from pathlib import Path

from slam.data_manager.factory.data_reader_ABC import DataReader
from slam.data_manager.factory.element import Element, RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.data_manager.factory.readers.ros2_reader.rosbags_reader import RosbagsManager
from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import Ros2Config
from slam.system_configs.system.data_manager.batch_factory.regime import (
    Stream,
    TimeLimit,
)
from slam.system_configs.system.setup_manager.sensors import SensorConfig


class Ros2DataReader(DataReader):
    """Data reader for ROS2 in test."""

    def __init__(self, regime: TimeLimit | Stream, dataset_params: Ros2Config):
        self._dataset_directory: Path = dataset_params.directory
        self._regime = regime



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




if __name__ == "__main__":

    print("Testing ROS2 data reader")
    folder_path = Path(os.environ['DATA_DIR'])
    bag_path = Path('{}/rosbag2_2024_1713944720'.format(folder_path))

    first_sensor_config = SensorConfig("left_camera_rgba")
    sensor_factory = SensorsFactory()

    first_sensor = Sensor(first_sensor_config)
    first_sensor_loc = Location()
    test_measurement = RawMeasurement(sensor=first_sensor, values=10)

    rb_manager = RosbagsManager(bag_path)
    topic_list, data_table = rb_manager.rosbag_read(num_readings=20)

    for topic in topic_list:
        print(topic.split('/'))

    for element in data_table:
        topic = element[1].split('/')[-1]




    timelimit = TimeLimit(start=10, stop=20)
    ros2_config = Ros2Config(directory=bag_path)
    Ros2DataReader(regime=timelimit, dataset_params=ros2_config)

    