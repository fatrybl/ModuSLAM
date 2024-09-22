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
timestamp5 = 1698927497190095250  # 100 sensor readings

timelimit1 = TimeLimit(start=timestamp1, stop=timestamp5)

sensors_table1 = {
    "stereo_camera_left": "left",
    "stereo_camera_right": "right",
    "imu": "xsens",
    "lidar_left": "vlp16l",
    "lidar_right": "vlp16r",
    "lidar_center": "vlp32c",
}


sensors1 = [Sensor(SensorConfig(sensor_name)) for sensor_name in list(sensors_table1.keys())]

print(sensors1)

dataset_cfg1 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table1)

stream = Stream()

sensors_factory_config1 = generate_sensors_factory_config(sensors1)


incorrect_sensors_factory_config = generate_sensors_factory_config([])

valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg1, stream, Ros2DataReader, elements),
)

valid_time_limit_scenarios = (
    (sensors_factory_config1, dataset_cfg1, timelimit1, Ros2DataReader, elements),
)


ros1 = (*valid_time_limit_scenarios,)
