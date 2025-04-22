from src.moduslam.data_manager.batch_factory.data_objects import Element
from src.moduslam.data_manager.batch_factory.data_readers.locations import Location
from src.tests.moduslam.data_manager.batch_factory.readers.tum_vie.scenarios.data import (
    dataset_cfg,
    el2,
    el3,
    el10,
    el12,
    el19,
    el22,
    el23,
    el24,
    elements,
)

invalid_element = Element(timestamp=el3.timestamp, measurement=el3.measurement, location=Location())

valid_scenarios = (
    (dataset_cfg, elements, elements),
    (dataset_cfg, [el3, el10, el23], [el3, el10, el23]),
    (dataset_cfg, [el2, el12], [el2, el12]),
    (dataset_cfg, [el19, el22, el24], [el19, el22, el24]),
    (dataset_cfg, elements[10:15], elements[10:15]),
)

invalid_scenario = (dataset_cfg, [invalid_element])
