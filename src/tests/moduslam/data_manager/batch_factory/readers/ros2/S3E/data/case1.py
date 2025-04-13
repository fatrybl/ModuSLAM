from src.moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2HumbleConfig,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.sensors import Sensor
from src.tests.conftest import s3e_dataset_dir
from src.tests_data_generators.ros2.s3e_dataset.data import Data, sensors_configs

data = Data(s3e_dataset_dir)
elements = data.elements

all_sensors: list[Sensor] = [element.measurement.sensor for element in elements]

dataset_cfg = Ros2HumbleConfig(
    directory=s3e_dataset_dir, sensor_topic_mapping=data.sensor_name_topic_map
)

stream = Stream()
t_limit_1 = TimeLimit(elements[0].timestamp, elements[-1].timestamp)
t_limit_2 = TimeLimit(elements[0].timestamp, elements[0].timestamp)
t_limit_3 = TimeLimit(elements[-1].timestamp, elements[-1].timestamp)
t_limit_4 = TimeLimit(elements[0].timestamp, elements[-10].timestamp)
t_limit_5 = TimeLimit(elements[10].timestamp, elements[-1].timestamp)
t_limit_6 = TimeLimit(elements[5].timestamp, elements[15].timestamp)

valid_stream_scenarios = ((sensors_configs, dataset_cfg, stream, elements),)

valid_timelimit_scenarios = (
    (sensors_configs, dataset_cfg, t_limit_1, elements),
    (sensors_configs, dataset_cfg, t_limit_2, [elements[0]]),
    (sensors_configs, dataset_cfg, t_limit_3, [elements[-1]]),
    (sensors_configs, dataset_cfg, t_limit_4, elements[:-10]),
    (sensors_configs, dataset_cfg, t_limit_5, elements[10:]),
    (sensors_configs, dataset_cfg, t_limit_6, elements[5:15]),
)

S3E_1 = (
    *valid_stream_scenarios,
    *valid_timelimit_scenarios,
)
