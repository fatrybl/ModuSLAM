from moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from test_data_generators.tum_vie_dataset.data import Data
from test_data_generators.utils import generate_sensors_factory_config
from tests.conftest import tum_vie_dataset_dir

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

timelimit1 = TimeLimit(start=el1.timestamp, stop=el24.timestamp)
timelimit2 = TimeLimit(start=el1.timestamp, stop=el11.timestamp)
timelimit3 = TimeLimit(start=el11.timestamp, stop=el24.timestamp)
timelimit4 = TimeLimit(start=el2.timestamp, stop=el10.timestamp)
timelimit5 = TimeLimit(start=el5.timestamp, stop=el5.timestamp)
timelimit6 = TimeLimit(start=el24.timestamp, stop=el24.timestamp)
timelimit7 = TimeLimit(start=el12.timestamp, stop=el23.timestamp)

sensors_factory_config1 = generate_sensors_factory_config((imu, stereo))
sensors_factory_config2 = generate_sensors_factory_config((imu,))
sensors_factory_config3 = generate_sensors_factory_config((stereo,))
incorrect_sensors_factory_config = generate_sensors_factory_config([])


invalid_stream_scenario = (
    incorrect_sensors_factory_config,
    dataset_cfg,
    regime,
    TumVieReader,
    [None],
)

valid_stream_scenarios = (
    (sensors_factory_config1, dataset_cfg, regime, TumVieReader, elements),
    (sensors_factory_config2, dataset_cfg, regime, TumVieReader, elements[1:10] + elements[11:23]),
    (sensors_factory_config3, dataset_cfg, regime, TumVieReader, [el1, el11, el24]),
)

valid_timelimit_scenarios = (
    (sensors_factory_config1, dataset_cfg, timelimit1, TumVieReader, elements),
    (sensors_factory_config1, dataset_cfg, timelimit2, TumVieReader, elements[:11]),
    (sensors_factory_config1, dataset_cfg, timelimit3, TumVieReader, elements[10:]),
    (sensors_factory_config2, dataset_cfg, timelimit4, TumVieReader, elements[1:10]),
    (sensors_factory_config2, dataset_cfg, timelimit5, TumVieReader, [el5]),
    (sensors_factory_config3, dataset_cfg, timelimit6, TumVieReader, [el24]),
    (sensors_factory_config2, dataset_cfg, timelimit7, TumVieReader, elements[11:23]),
)

invalid_timelimit_scenarios = (
    (incorrect_sensors_factory_config, dataset_cfg, timelimit1, TumVieReader, [None]),
    (sensors_factory_config3, dataset_cfg, timelimit4, TumVieReader, [None]),
)

stream_scenarios = (
    *valid_stream_scenarios,
    invalid_stream_scenario,
)

time_limit_scenarios = (
    *valid_timelimit_scenarios,
    *invalid_timelimit_scenarios,
)

tum_vie1 = (
    *stream_scenarios,
    *time_limit_scenarios,
)
