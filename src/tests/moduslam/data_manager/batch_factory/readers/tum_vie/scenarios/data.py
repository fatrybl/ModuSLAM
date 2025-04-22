from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.sensors import Sensor
from src.tests.conftest import tum_vie_dataset_dir
from src.tests_data_generators.tum_vie_dataset.data import Data
from src.tests_data_generators.utils import generate_sensors_factory_config
from src.utils.auxiliary_methods import nanosec2microsec

dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
data = Data(dataset_cfg)
elements = data.elements

imu = data.imu
stereo = data.stereo

all_sensors: list[Sensor] = [element.measurement.sensor for element in elements]

stream = Stream()

el1 = elements[0]  # stereo
el2 = elements[1]  # imu
el3 = elements[2]  # imu
el5 = elements[4]  # imu
el10 = elements[9]  # imu
el11 = elements[10]  # stereo
el12 = elements[11]  # imu
el19 = elements[18]  # imu
el22 = elements[21]  # imu
el23 = elements[22]  # imu
el24 = elements[23]  # stereo

timelimit1 = TimeLimit(start=nanosec2microsec(el1.timestamp), stop=nanosec2microsec(el24.timestamp))
timelimit2 = TimeLimit(start=nanosec2microsec(el1.timestamp), stop=nanosec2microsec(el11.timestamp))
timelimit3 = TimeLimit(
    start=nanosec2microsec(el11.timestamp), stop=nanosec2microsec(el24.timestamp)
)
timelimit4 = TimeLimit(start=nanosec2microsec(el2.timestamp), stop=nanosec2microsec(el10.timestamp))
timelimit5 = TimeLimit(start=nanosec2microsec(el5.timestamp), stop=nanosec2microsec(el5.timestamp))
timelimit6 = TimeLimit(
    start=nanosec2microsec(el24.timestamp), stop=nanosec2microsec(el24.timestamp)
)
timelimit7 = TimeLimit(
    start=nanosec2microsec(el12.timestamp), stop=nanosec2microsec(el23.timestamp)
)

sensors_factory_config1 = generate_sensors_factory_config((imu, stereo))
sensors_factory_config2 = generate_sensors_factory_config((imu,))
sensors_factory_config3 = generate_sensors_factory_config((stereo,))
