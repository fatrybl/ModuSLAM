from src.moduslam.data_manager.batch_factory.readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.sensors import Sensor
from src.tests.conftest import tum_vie_dataset_dir
from src.tests_data_generators.tum_vie_dataset.data import Data
from src.tests_data_generators.utils import generate_sensors_factory_config
from src.utils.auxiliary_methods import nanosec2microsec

dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
data = Data(dataset_cfg)
elements = data.elements

all_sensors: list[Sensor] = [element.measurement.sensor for element in elements]

imu = data.imu
stereo = data.stereo

stream = Stream()

el1 = elements[0]  # stereo
el2 = elements[1]  # imu
el3 = elements[2]  # imu
el4 = elements[3]  # imu
el5 = elements[4]  # imu
el10 = elements[9]  # imu
el11 = elements[10]  # stereo
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
    start=nanosec2microsec(el10.timestamp), stop=nanosec2microsec(el23.timestamp)
)

sensors_factory_config1 = generate_sensors_factory_config((imu, stereo))
sensors_factory_config2 = generate_sensors_factory_config((imu,))
sensors_factory_config3 = generate_sensors_factory_config((stereo,))


valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg, stream, TumVieReader, all_sensors, elements),
    (sensors_factory_config2, dataset_cfg, stream, TumVieReader, [imu, imu, imu], [el2, el3, el4]),
    (sensors_factory_config3, dataset_cfg, stream, TumVieReader, [stereo], [el1]),
    (
        sensors_factory_config3,
        dataset_cfg,
        stream,
        TumVieReader,
        [stereo, stereo, stereo],
        [el1, el11, el24],
    ),
    (
        sensors_factory_config2,
        dataset_cfg,
        stream,
        TumVieReader,
        [element.measurement.sensor for element in (elements[1:10] + elements[11:])],
        elements[1:10] + elements[11:23],
    ),
)


valid_timelimit_scenarios = (
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit1,
        TumVieReader,
        all_sensors,
        elements,
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit2,
        TumVieReader,
        [element.measurement.sensor for element in elements[0:11]],
        elements[0:11],
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit3,
        TumVieReader,
        [element.measurement.sensor for element in elements[10:]],
        elements[10:],
    ),
    (
        sensors_factory_config2,
        dataset_cfg,
        timelimit4,
        TumVieReader,
        [element.measurement.sensor for element in elements[1:10]],
        elements[1:10],
    ),
    (
        sensors_factory_config2,
        dataset_cfg,
        timelimit5,
        TumVieReader,
        [el5.measurement.sensor],
        [el5],
    ),
    (
        sensors_factory_config3,
        dataset_cfg,
        timelimit6,
        TumVieReader,
        [el24.measurement.sensor],
        [el24],
    ),
    (
        sensors_factory_config1,
        dataset_cfg,
        timelimit7,
        TumVieReader,
        [element.measurement.sensor for element in elements[9:23]],
        elements[9:23],
    ),
)

tum_vie2 = (*valid_stream_scenarios, *valid_timelimit_scenarios)
