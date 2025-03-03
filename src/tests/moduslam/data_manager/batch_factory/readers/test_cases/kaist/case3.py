from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from src.moduslam.data_manager.batch_factory.readers.locations import Location
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
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

stream = Stream()

timelimit1 = TimeLimit(start=elements[0].timestamp, stop=elements[-1].timestamp)
timelimit2 = TimeLimit(start=el3.timestamp, stop=el23.timestamp)
timelimit3 = TimeLimit(start=el2.timestamp, stop=el12.timestamp)
timelimit4 = TimeLimit(start=el19.timestamp, stop=el24.timestamp)
timelimit5 = TimeLimit(start=el5.timestamp, stop=el25.timestamp)
timelimit6 = TimeLimit(start=el3.timestamp, stop=el8.timestamp)

all_sensors: list[Sensor] = [element.measurement.sensor for element in elements]
sensors_factory_config1 = generate_sensors_factory_config(all_sensors)
sensors_factory_config2 = generate_sensors_factory_config([imu])
sensors_factory_config3 = generate_sensors_factory_config([lidar2D_back])
sensors_factory_config4 = generate_sensors_factory_config([stereo])
sensors_factory_config5 = generate_sensors_factory_config([lidar2D_middle])
sensors_factory_config6 = generate_sensors_factory_config([imu, altimeter])
incorrect_sensors_factory_config = generate_sensors_factory_config([])

invalid_element = Element(timestamp=el3.timestamp, measurement=el3.measurement, location=Location())


valid_scenarios = (
    (sensors_factory_config1, dataset_cfg, timelimit6, KaistReader, elements, elements),
    (
        sensors_factory_config2,
        dataset_cfg,
        timelimit6,
        KaistReader,
        [el3, el10, el23],
        [el3, el10, el23],
    ),
    (
        sensors_factory_config3,
        dataset_cfg,
        stream,
        KaistReader,
        [el2, el12],
        [el2, el12],
    ),
    (
        sensors_factory_config4,
        dataset_cfg,
        timelimit4,
        KaistReader,
        [el19, el22, el24],
        [el19, el22, el24],
    ),
    (
        sensors_factory_config5,
        dataset_cfg,
        stream,
        KaistReader,
        [el5, el14, el25],
        [el5, el14, el25],
    ),
)

invalid_scenario = (
    sensors_factory_config2,
    dataset_cfg,
    stream,
    KaistReader,
    [invalid_element],
    [Exception],
)
"""TODO: handle more precise exception."""

out_of_context = (sensors_factory_config1, dataset_cfg, stream, KaistReader, el3)

kaist_success = (*valid_scenarios,)
kaist_invalid_element = (*invalid_scenario,)
kaist_out_of_context = (*out_of_context,)
