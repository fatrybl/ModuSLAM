import os
from dataclasses import dataclass, field
from pathlib import Path

from moduslam.data_manager.factory.readers.ros2.get_data import DataGrabber
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from moduslam.system_configs.setup_manager.sensors import SensorConfig, ImuConfig


@dataclass
class Iterator:
    """Iterator for the sensor`s timestamp file."""

    bagpath: Path
    # msg_limit:int = 10000
    position: int = 0
    data: list = None
    sensors: dict = field(default_factory=lambda: {"Imu": ["xsens"]})

    def sensor_config_setup(self):
        configs: dict[str, SensorConfig] = {}
        for sensor_type, sensor_names in self.sensors.items():
            for sensor in sensor_names:
                print(sensor_type, sensor)  # Imu, xsens
                imu_cfg = ImuConfig(name="imu", type_name="Imu")
                configs[sensor] = imu_cfg

        my_config = SensorFactoryConfig(sensors=configs)
        print(configs)

        SensorsFactory.init_sensors(config=my_config)

    def reset(self):
        self.position = 0
        self._get_data(self.position)

    def _get_data(self, pos: int):
        return DataGrabber.iter_rosbag(self.bagpath, pos)

    def next(self):
        self.position += 1
        try:
            data_read, timestamp = self._get_data(self.position)
            sensor_device = data_read[1].split("/")[1]

            for sensor in self.sensors.keys():
                if sensor_device in self.sensors[sensor]:
                    sensor_name = sensor

            sensor: Sensor = SensorsFactory.get_sensor(sensor_name)
            # sensor = data_read, iter_pos
            return sensor, timestamp, self.position

        except StopIteration:
            print("Sensor not found")


if __name__ == "__main__":

    folder_path = Path(os.environ["DATA_DIR"])
    bag_path = Path("{}/rosbag2_2023_11_02-12_18_16".format(folder_path))

    my_iterator = Iterator(bag_path)
    my_iterator.sensor_config_setup()
    (sensor, t), iterator = my_iterator.next()
