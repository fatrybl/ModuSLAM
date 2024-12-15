from phd.moduslam.data_manager.batch_factory.readers.tum_vie.configs.base import (
    TumVieConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from phd.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from phd.moduslam.utils.auxiliary_methods import nanosec2microsec
from phd.tests.conftest import tum_vie_dataset_dir
from phd.tests_data_generators.tum_vie_dataset.data import Data
from phd.tests_data_generators.utils import generate_sensors_factory_config

dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
data = Data(dataset_cfg)
elements = data.elements

imu = data.imu
stereo = data.stereo

regime = Stream()

el1 = elements[0]  # stereo
el2 = elements[1]  # imu
el5 = elements[4]  # imu
el10 = elements[9]  # imu
el11 = elements[10]  # stereo
el12 = elements[11]  # imu
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

valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg, regime, TumVieReader, elements),
    (sensors_factory_config2, dataset_cfg, regime, TumVieReader, elements[1:10] + elements[11:23]),
    (sensors_factory_config3, dataset_cfg, regime, TumVieReader, [el1, el11, el24, None]),
)

valid_timelimit_scenarios = (
    (sensors_factory_config1, dataset_cfg, timelimit1, TumVieReader, elements),
    (sensors_factory_config1, dataset_cfg, timelimit2, TumVieReader, elements[:11]),
    (sensors_factory_config1, dataset_cfg, timelimit3, TumVieReader, elements[10:]),
    (sensors_factory_config2, dataset_cfg, timelimit4, TumVieReader, elements[1:10]),
    (sensors_factory_config2, dataset_cfg, timelimit5, TumVieReader, [el5, None]),
    (sensors_factory_config3, dataset_cfg, timelimit6, TumVieReader, [el24, None]),
    (sensors_factory_config2, dataset_cfg, timelimit7, TumVieReader, elements[11:23]),
)

tum_vie1 = (
    *valid_stream_scenarios,
    *valid_timelimit_scenarios,
)
