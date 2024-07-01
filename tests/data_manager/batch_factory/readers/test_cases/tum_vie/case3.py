from moduslam.data_manager.batch_factory.batch import Element
from moduslam.data_manager.batch_factory.readers.locations import Location
from moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream
from test_data_generators.tum_vie_dataset.data import Data
from test_data_generators.utils import generate_sensors_factory_config
from tests.conftest import tum_vie_dataset_dir

dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
data = Data(dataset_cfg)
elements = data.elements

imu = data.imu
stereo = data.stereo

stream = Stream()

el2 = elements[1]  # imu
el3 = elements[2]  # imu
el10 = elements[9]  # imu
el12 = elements[11]  # imu
el19 = elements[18]  # imu
el22 = elements[21]  # imu
el23 = elements[22]  # imu
el24 = elements[23]  # stereo

sensors_factory_config1 = generate_sensors_factory_config((imu, stereo))


invalid_element = Element(timestamp=el3.timestamp, measurement=el3.measurement, location=Location())


valid_scenarios = (
    (sensors_factory_config1, dataset_cfg, stream, TumVieReader, elements, elements),
    (
        sensors_factory_config1,
        dataset_cfg,
        stream,
        TumVieReader,
        [el3, el10, el23],
        [el3, el10, el23],
    ),
    (sensors_factory_config1, dataset_cfg, stream, TumVieReader, [el2, el12], [el2, el12]),
    (
        sensors_factory_config1,
        dataset_cfg,
        stream,
        TumVieReader,
        [el19, el22, el24],
        [el19, el22, el24],
    ),
    (sensors_factory_config1, dataset_cfg, stream, TumVieReader, elements[10:15], elements[10:15]),
)

invalid_scenario = (
    sensors_factory_config1,
    dataset_cfg,
    stream,
    TumVieReader,
    [invalid_element],
    [Exception],
)


tum_vie_success = (*valid_scenarios,)
tum_vie_fail = (invalid_scenario,)
