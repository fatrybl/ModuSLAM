from moduslam.data_manager.batch_factory.data_objects import Element
from moduslam.data_manager.batch_factory.data_readers.locations import Location
from tests.moduslam.data_manager.batch_factory.readers.kaist_urban.scenarios.data import (
    dataset_cfg,
    el2,
    el3,
    el5,
    el10,
    el12,
    el14,
    el19,
    el22,
    el23,
    el24,
    el25,
    elements,
)

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
