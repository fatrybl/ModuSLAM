from moduslam.data_manager.batch_factory.readers.ros2.reader import Ros2DataReader
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from tests.conftest import ros2_dataset_dir
from tests_data_generators.ros2_dataset.data import elements
from tests_data_generators.utils import generate_sensors_factory_config

timestamp1 = 1698927496694557229
timestamp2 = 1698927497652542865
timestamp3 = 1698927498123884925
timestamp4 = 1698927499116096802
timestamp5 = 1698927499980874274

timelimit1 = TimeLimit(start=timestamp1, stop=timestamp5)
timelimit2 = TimeLimit(start=timestamp2, stop=timestamp5)
timelimit3 = TimeLimit(start=timestamp1, stop=timestamp4)
timelimit4 = TimeLimit(start=timestamp2, stop=timestamp4)
timelimit5 = TimeLimit(start=timestamp3, stop=timestamp5)

sensors_table1 = {
    "stereo_camera_left": "left",
    "stereo_camera_right": "right",
    "imu": "imu",
    "lidar_left": "vlp16l",
    "lidar_right": "vlp16r",
    "lidar_center": "vlp32c",
}

sensors_table2 = {
    "stereo_camera_left": "left",
    "imu": "imu",
    "lidar_center": "vlp32c",
}

sensors_table3 = {
    "stereo_camera_left": "left",
    "stereo_camera_right": "right",
}

sensors_table4 = {
    "imu": "imu",
}

sensors_table5 = {
    "lidar_left": "vlp16l",
    "lidar_right": "vlp16r",
    "lidar_center": "vlp32c",
}

sensors1 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table1.keys())]
sensors2 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table2.values())]
sensors3 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table3.values())]
sensors4 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table4.values())]
sensors5 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table5.values())]

print(sensors1)

dataset_cfg1 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table1)
dataset_cfg2 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table2)
dataset_cfg3 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table3)
dataset_cfg4 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table4)
dataset_cfg5 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table5)

stream = Stream()

sensors_factory_config1 = generate_sensors_factory_config(sensors1)
sensors_factory_config2 = generate_sensors_factory_config(sensors2)
sensors_factory_config3 = generate_sensors_factory_config(sensors3)
sensors_factory_config4 = generate_sensors_factory_config(sensors4)
sensors_factory_config5 = generate_sensors_factory_config(sensors5)

print("List of configs for sensors")
print(sensors_factory_config1)

print("elements are:")
print(elements)

incorrect_sensors_factory_config = generate_sensors_factory_config([])

valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg1, stream, Ros2DataReader, elements),
)

valid_time_limit_scenarios = (
    (sensors_factory_config1, dataset_cfg1, timelimit1, Ros2DataReader, elements),
)


ros1 = (*valid_time_limit_scenarios,)
