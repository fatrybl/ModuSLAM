from src.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from src.moduslam.data_manager.batch_factory.data_readers.locations import (
    Ros2DataLocation,
)
from src.tests.moduslam.data_manager.batch_factory.readers.ros2.scenarios.s3e_data import (
    dataset_cfg,
    elements,
    shuffled_elements,
)
from src.tests_data_generators.ros2.s3e_dataset.data import imu

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
