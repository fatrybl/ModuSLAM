from moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.sensors_factory.sensors import Sensor
from tests.conftest import kaist_custom_dataset_dir
from tests.tests_data_generators.kaist_dataset.data import Data
from tests.tests_data_generators.utils import generate_sensors_factory_config

data = Data(kaist_custom_dataset_dir)
elements = data.elements

el1 = elements[0]
el2 = elements[1]
el3 = elements[2]
el5 = elements[4]
el8 = elements[7]
el10 = elements[9]
el12 = elements[11]
el14 = elements[13]
el19 = elements[18]
el22 = elements[21]
el23 = elements[22]
el24 = elements[23]
el25 = elements[24]

imu = data.imu
stereo = data.stereo
lidar2D_back = data.sick_back
lidar2D_middle = data.sick_middle
lidar3D_left = data.velodyne_left
lidar3D_right = data.velodyne_right
altimeter = data.altimeter

dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)

all_sensors: list[Sensor] = [element.measurement.sensor for element in elements]

stream = Stream()

timelimit1 = TimeLimit(start=el1.timestamp, stop=el25.timestamp)
timelimit2 = TimeLimit(start=el3.timestamp, stop=el23.timestamp)
timelimit3 = TimeLimit(start=el2.timestamp, stop=el12.timestamp)
timelimit4 = TimeLimit(start=el19.timestamp, stop=el24.timestamp)
timelimit5 = TimeLimit(start=el5.timestamp, stop=el25.timestamp)
timelimit6 = TimeLimit(start=el3.timestamp, stop=el8.timestamp)
timelimit7 = TimeLimit(start=el3.timestamp, stop=el10.timestamp)

sensors_factory_config1 = generate_sensors_factory_config(all_sensors)
sensors_factory_config2 = generate_sensors_factory_config([imu])
sensors_factory_config3 = generate_sensors_factory_config([lidar2D_back])
sensors_factory_config4 = generate_sensors_factory_config([stereo])
sensors_factory_config5 = generate_sensors_factory_config([lidar2D_middle])
sensors_factory_config6 = generate_sensors_factory_config([imu, altimeter])

incorrect_sensors_factory_config = generate_sensors_factory_config([])
