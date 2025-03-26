from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.data_readers.locations import Location
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.tests.conftest import tum_vie_dataset_dir
from src.tests_data_generators.tum_vie_dataset.data import Data

dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
data = Data(dataset_cfg)
elements = data.elements

imu = data.imu
stereo = data.stereo

el2 = elements[1]  # imu
el3 = elements[2]  # imu
el10 = elements[9]  # imu
el12 = elements[11]  # imu
el19 = elements[18]  # imu
el22 = elements[21]  # imu
el23 = elements[22]  # imu
el24 = elements[23]  # stereo

invalid_element = Element(timestamp=el3.timestamp, measurement=el3.measurement, location=Location())

valid_scenarios = (
    (dataset_cfg, elements, elements),
    (dataset_cfg, [el3, el10, el23], [el3, el10, el23]),
    (dataset_cfg, [el2, el12], [el2, el12]),
    (dataset_cfg, [el19, el22, el24], [el19, el22, el24]),
    (dataset_cfg, elements[10:15], elements[10:15]),
)

invalid_scenario = (dataset_cfg, [invalid_element], [Exception])

out_of_context = (dataset_cfg, el3)
