from tests.moduslam.data_manager.batch_factory.readers.ros2.scenarios.s3e_data import (
    dataset_cfg,
    elements,
    invalid_element_1,
    invalid_element_2,
    shuffled_elements,
)

valid_scenarios = (
    (dataset_cfg, elements, elements),
    (dataset_cfg, shuffled_elements, shuffled_elements),
)

invalid_scenarios = (
    (dataset_cfg, [invalid_element_1]),
    (dataset_cfg, [invalid_element_2]),
)
