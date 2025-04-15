import random

from src.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from src.moduslam.data_manager.batch_factory.data_readers.locations import (
    Ros2DataLocation,
)
from src.moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2HumbleConfig,
)
from src.tests.conftest import s3e_dataset_dir
from src.tests_data_generators.ros2.s3e_dataset.data import (
    Data,
    imu,
    sensor_name_topic_map,
)

data = Data(s3e_dataset_dir)
elements = data.elements
shuffled_elements = random.sample(elements, len(elements))

dataset_cfg = Ros2HumbleConfig(
    directory=s3e_dataset_dir, sensor_topic_mapping=sensor_name_topic_map
)

valid_stream_scenarios = (
    (dataset_cfg, elements, elements),
    (dataset_cfg, shuffled_elements, shuffled_elements),
)

invalid_element = Element(
    timestamp=1,
    measurement=RawMeasurement(imu, "some data"),
    location=Ros2DataLocation("some topic"),
)
invalid_scenario = (dataset_cfg, [invalid_element])
