from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.locations import Location
from src.moduslam.sensors_factory.sensors import Sensor
from src.tests.conftest import kaist_custom_dataset_dir
from src.tests_data_generators.kaist_dataset.data import Data
from src.tests_data_generators.utils import generate_sensors_factory_config

data = Data(kaist_custom_dataset_dir)
elements = data.elements
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
incorrect_sensors_factory_config = generate_sensors_factory_config([])

unallocated_element = Element(
    timestamp=el3.timestamp, measurement=el3.measurement, location=Location()
)

valid_scenarios = (
    (dataset_cfg, elements, elements),
    (dataset_cfg, [el3, el10, el23], [el3, el10, el23]),
    (dataset_cfg, [el2, el12], [el2, el12]),
    (dataset_cfg, [el19, el22, el24], [el19, el22, el24]),
    (dataset_cfg, [el5, el14, el25], [el5, el14, el25]),
)

invalid_scenario = (dataset_cfg, [unallocated_element])
