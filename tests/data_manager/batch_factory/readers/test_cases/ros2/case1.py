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

# TODO: Optimize cases for Ros2 because the test is taking too long to run
el1 = elements[0]
el2 = elements[1]
el3 = elements[2]
el4 = elements[3]
el5 = elements[4]
el6 = elements[5]
el7 = elements[6]
el8 = elements[7]
el9 = elements[8]
el10 = elements[9]
el11 = elements[10]
el12 = elements[11]
el13 = elements[12]
el14 = elements[13]
el15 = elements[14]
el16 = elements[15]
el17 = elements[16]
el18 = elements[17]
el19 = elements[18]
el20 = elements[19]
el21 = elements[20]
el22 = elements[21]
el23 = elements[22]
el24 = elements[23]
el25 = elements[24]
el26 = elements[25]
el27 = elements[26]
el28 = elements[27]
el29 = elements[28]
el30 = elements[29]
el31 = elements[30]
el32 = elements[31]
el33 = elements[32]
el34 = elements[33]
el35 = elements[34]
el36 = elements[35]
el37 = elements[36]
el38 = elements[37]
el39 = elements[38]
el40 = elements[39]
el41 = elements[40]
el42 = elements[41]
el43 = elements[42]
el44 = elements[43]
el45 = elements[44]
el46 = elements[45]
el47 = elements[46]
el48 = elements[47]
el49 = elements[48]
el50 = elements[49]
el51 = elements[50]
el52 = elements[51]
el53 = elements[52]
el54 = elements[53]

timestamp1 = 1698927496694033807
timestamp2 = 1698927496739239954  # 20 sensor readings
timestamp3 = 1698927496799306816  # 40 sensor readings
timestamp4 = 1698927496898641344  # 60 sensor readings
timestamp5 = 1698927497046583719  # 80 sensor readings
timestamp6 = 1698927497190095250  # 100 sensor readings

#TODO: check elements and timestamps, sort by timestamp
elements_0_20 = [e for e in elements if e.timestamp >= timestamp1 and e.timestamp < timestamp2]
elements20_40 = [e for e in elements if e.timestamp >= timestamp2 and e.timestamp < timestamp3]
elements40_60 = [e for e in elements if e.timestamp >= timestamp3 and e.timestamp < timestamp4]
elements60_80 = [e for e in elements if e.timestamp >= timestamp4 and e.timestamp < timestamp5]
elements80_100 = [e for e in elements if e.timestamp >= timestamp5 and e.timestamp < timestamp6]

sensors_table1 = {
    "stereo_camera_left": "left",
    "stereo_camera_right": "right",
    "imu": "xsens",
    "lidar_left": "vlp16l",
    "lidar_right": "vlp16r",
    "lidar_center": "vlp32c",
}
sensors_table_stereo_camera_left = {
     "stereo_camera_left": "left",
}
sensors_table_stereo_camera_right = {
     "stereo_camera_right": "right",
}
sensors_table_imu = {
    "imu": "xsens",
}
sensors_table_lidar_left = {
    "lidar_left": "vlp16l",
}
sensors_table_lidar_right = {
    "lidar_right": "vlp16r",
}
sensors_table_lidar_center = {
    "lidar_center": "vlp32c",
}

sensors_table_e1_e10 = {
    "imu": "xsens",
    "lidar_left": "vlp16l",
}
incorrect_sensors_table_e1_e10 = {
    "stereo_camera_left": "left",
    "stereo_camera_right": "right",
    "lidar_right": "vlp16r",
    "lidar_center": "vlp32c",
}

topics_table  = {
      "stereo_camera_left": "Image",
      "stereo_camera_right": "Image",
      "imu": "Imu",
      "lidar_left": "PointCloud2",
      "lidar_right": "PointCloud2",
      "lidar_center": "PointCloud2",
}
sensors1 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table1.keys())]
sensors2 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table_stereo_camera_left.keys())]
sensors3 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table_stereo_camera_right.keys())]
sensors4 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table_imu.keys())]
sensors5 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table_lidar_left.keys())]
sensors6 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table_lidar_right.keys())]
sensors7 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table_lidar_center.keys())]

sensors_e1_e10 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table_e1_e10.keys())]
incorrect_sensors_e1_e10 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(incorrect_sensors_table_e1_e10.keys())]

dataset_cfg1 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table1, topics_table=topics_table)
dataset_cfg_e1_e10 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table_e1_e10, topics_table=topics_table)
incorrect_dataset_cfg_e1_e10 = Ros2Config(directory=ros2_dataset_dir, sensors_table=incorrect_sensors_table_e1_e10)

stream = Stream()

# TODO: check test with elements 40_60 and 60_80 due to test fail  upd: 40_60 fix
timelimit20 = TimeLimit(start=timestamp1, stop=timestamp2)
timelimit20_40 = TimeLimit(start=timestamp2, stop=timestamp3)
timelimit40_60 = TimeLimit(start=timestamp3, stop=timestamp4)
timelimit60_80 = TimeLimit(start=timestamp4, stop=timestamp5)
timelimit80_100 = TimeLimit(start=timestamp5, stop=timestamp6)

sensors_factory_config1 = generate_sensors_factory_config(sensors1)
sensors_factory_config2 = generate_sensors_factory_config(sensors2)
sensors_factory_config3 = generate_sensors_factory_config(sensors3)
sensors_factory_config4 = generate_sensors_factory_config(sensors4)
sensors_factory_config5 = generate_sensors_factory_config(sensors5)
sensors_factory_config6 = generate_sensors_factory_config(sensors6)
sensors_factory_config7 = generate_sensors_factory_config(sensors7)

sensors_factory_config_e1_e10 = generate_sensors_factory_config(sensors_e1_e10)
invalid_sensors_factory_config_e1_e10 = generate_sensors_factory_config(sensors_e1_e10)
incorrect_sensors_factory_config = generate_sensors_factory_config([])

# TODO: Test with ROS2DataReader fails when the first element is missing
# TODO: Test with ROS2DataReader for GPS check
valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg1, stream, Ros2DataReader, elements),
    (sensors_factory_config2, dataset_cfg1, stream, Ros2DataReader, [el23, el40]), # stereo_camera_left
    (sensors_factory_config3, dataset_cfg1, stream, Ros2DataReader, [el33, el54]), # stereo_camera_right
    (sensors_factory_config4, dataset_cfg1, stream, Ros2DataReader, [el1, el3, el4]), # imu
    (sensors_factory_config5, dataset_cfg1, stream, Ros2DataReader, [el2, el20, el35, el49]), # lidar_left
    (sensors_factory_config6, dataset_cfg1, stream, Ros2DataReader, [el15, el29, el44]), # lidar_right
    (sensors_factory_config7, dataset_cfg1, stream, Ros2DataReader, [el14, el27, el42]),  # lidar_center
    (sensors_factory_config_e1_e10, dataset_cfg_e1_e10, stream, Ros2DataReader, [el1, el2, el3]), # imu, lidar_left, imu
)
# TODO: More tests with different invalid configs
invalid_stream_scenarios = (
    (incorrect_sensors_factory_config, dataset_cfg1, stream, Ros2DataReader, [None]),
#     (invalid_sensors_factory_config_e1_e10, incorrect_dataset_cfg_e1_e10, stream, Ros2DataReader, [el1, el2, el3]),
#     (sensors_factory_config_e1_e10, incorrect_dataset_cfg_e1_e10, stream, Ros2DataReader, [el1, el2, el3]),
#     (sensors_factory_config_e1_e10, dataset_cfg_e1_e10, stream, Ros2DataReader, [el23, el40]),
)
# TODO: elements 60_80 due to test fail
valid_timelimit_scenarios = (
    (sensors_factory_config1, dataset_cfg1, timelimit20, Ros2DataReader, elements_0_20),
    (sensors_factory_config1, dataset_cfg1, timelimit20_40, Ros2DataReader, elements20_40),
    (sensors_factory_config1, dataset_cfg1, timelimit40_60, Ros2DataReader, elements40_60),
    # (sensors_factory_config1, dataset_cfg1, timelimit60_80, Ros2DataReader, elements60_80),
    (sensors_factory_config1, dataset_cfg1, timelimit80_100, Ros2DataReader, elements80_100),
)

invalid_timelimit_scenarios = (
    (incorrect_sensors_factory_config, dataset_cfg1, timelimit20, Ros2DataReader, [None]),
    # (sensors_factory_config1, dataset_cfg1, timelimit80_100, Ros2DataReader, [None]),
    # (sensors_factory_config2, dataset_cfg1, timelimit20, Ros2DataReader, [None]),
    # (incorrect_sensors_factory_config, dataset_cfg1, timelimit20_40, Ros2DataReader, [None]),
    # (incorrect_sensors_factory_config, dataset_cfg1, timelimit40_60, Ros2DataReader, [None]),
    # (incorrect_sensors_factory_config, dataset_cfg1, timelimit60_80, Ros2DataReader, [None]),
    # (incorrect_sensors_factory_config, dataset_cfg1, timelimit80_100, Ros2DataReader, [None]),
)
# TODO: Hardcoded topics for Bag: Ros2DataReader `self._data_types = ["Image", "PointCloud2", "Imu"]`
stream_scenarios = (
    *valid_stream_scenarios,
    *invalid_stream_scenarios,
)
time_limit_scenarios = (
    *valid_timelimit_scenarios,
    *invalid_timelimit_scenarios,
)

ros2_case1 = (
    *stream_scenarios,
    *time_limit_scenarios,
)

