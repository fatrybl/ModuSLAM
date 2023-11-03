from pathlib import Path

from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module
from configs.sensors.base_sensor_parameters import ParameterConfig


from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.kaist.data_classes import CsvDataLocation
from slam.setup_manager.sensor_factory.sensors import Encoder

from tests.data_manager.factory.readers.kaist.data_factory import SensorNamePath, DatasetStructure
from tests.data_manager.factory.readers.kaist.conftest import SENSOR_CONFIG_NAME, CONFIG_MODULE_DIR


cs = ConfigStore.instance()
cs.store(name=SENSOR_CONFIG_NAME, node=ParameterConfig)
with initialize_config_module(config_module=CONFIG_MODULE_DIR):
    params = compose(config_name=SENSOR_CONFIG_NAME)

DATASET_DIR: Path = DatasetStructure.DATASET_DIR

CALIBRATION_DATA_DIR: Path = DatasetStructure.CALIBRATION_DATA_DIR
SENSOR_DATA_DIR: Path = DatasetStructure.SENSOR_DATA_DIR
IMAGE_DATA_DIR: Path = DatasetStructure.IMAGE_DATA_DIR

DATA_STAMP_FILE: Path = DatasetStructure.DATA_STAMP_FILE

SICK_BACK_DIR: Path = DatasetStructure.SICK_BACK_DIR
SICK_MIDDLE_DIR: Path = DatasetStructure.SICK_MIDDLE_DIR
VLP_LEFT_DIR: Path = DatasetStructure.VLP_LEFT_DIR
VLP_RIGHT_DIR: Path = DatasetStructure.VLP_RIGHT_DIR
STEREO_LEFT_DIR: Path = DatasetStructure.STEREO_LEFT_DIR
STEREO_RIGHT_DIR: Path = DatasetStructure.STEREO_RIGHT_DIR

BINARY_FILE_EXTENSION: str = DatasetStructure.BINARY_FILE_EXTENSION
IMAGE_FILE_EXTENSION: str = DatasetStructure.IMAGE_FILE_EXTENSION

encoder = SensorNamePath('encoder', Path('encoder.csv'))

# data_stamp.csv file content. The order of the measurements.
data_stamp = [
    [1, encoder.name]
]

# raw measurements
z_encoder_1 = (1, 1.0, 1.0, 1.0)

element = Element(
    timestamp=z_encoder_1[0],
    measurement=Measurement(
        sensor=Encoder(encoder.name, params),
        values=tuple(str(i) for i in z_encoder_1[1:])),
    location=CsvDataLocation(
        file=SENSOR_DATA_DIR / encoder.file_path,
        position=0))
