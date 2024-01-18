from dataclasses import dataclass
from pathlib import Path

from hydra import compose, initialize_config_module
from hydra.core.config_store import ConfigStore

from configs.paths.kaist_dataset import KaistDatasetPathConfig
from configs.sensors.base_sensor_parameters import ParameterConfig
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.kaist.data_classes import CsvDataLocation
from slam.setup_manager.sensor_factory.sensors import Encoder
from tests.data_manager.auxiliary_utils.kaist_data_factory import SensorNamePath
from tests.data_manager.factory.readers.kaist.api.empty_dataset.config import (
    DATASET_DIR,
)
from tests.data_manager.factory.readers.kaist.conftest import SENSOR_FACTORY_CONFIG_NAME

cs = ConfigStore.instance()
cs.store(name=SENSOR_FACTORY_CONFIG_NAME, node=ParameterConfig)
with initialize_config_module(config_module="conf"):
    params = compose(config_name=SENSOR_FACTORY_CONFIG_NAME)


@dataclass(frozen=True)
class DatasetStructure:
    dataset_directory: Path = DATASET_DIR
    calibration_data_dir: Path = dataset_directory / KaistDatasetPathConfig.calibration_data_dir
    sensor_data_dir: Path = dataset_directory / KaistDatasetPathConfig.sensor_data_dir
    image_data_dir: Path = dataset_directory / KaistDatasetPathConfig.image_data_dir
    data_stamp: Path = dataset_directory / KaistDatasetPathConfig.data_stamp
    lidar_2D_back_dir: Path = dataset_directory / KaistDatasetPathConfig.lidar_2D_back_dir
    lidar_2D_middle_dir: Path = dataset_directory / KaistDatasetPathConfig.lidar_2D_middle_dir
    lidar_3D_left_dir: Path = dataset_directory / KaistDatasetPathConfig.lidar_3D_left_dir
    lidar_3D_right_dir: Path = dataset_directory / KaistDatasetPathConfig.lidar_3D_right_dir
    stereo_left_data_dir: Path = (
        dataset_directory / KaistDatasetPathConfig.image_data_dir / KaistDatasetPathConfig.stereo_left_data_dir
    )
    stereo_right_data_dir: Path = (
        dataset_directory / KaistDatasetPathConfig.image_data_dir / KaistDatasetPathConfig.stereo_right_data_dir
    )

    imu_data_file: Path = dataset_directory / KaistDatasetPathConfig.imu_data_file
    fog_data_file: Path = dataset_directory / KaistDatasetPathConfig.fog_data_file
    encoder_data_file: Path = dataset_directory / KaistDatasetPathConfig.encoder_data_file
    altimeter_data_file: Path = dataset_directory / KaistDatasetPathConfig.altimeter_data_file
    gps_data_file: Path = dataset_directory / KaistDatasetPathConfig.gps_data_file
    vrs_gps_data_file: Path = dataset_directory / KaistDatasetPathConfig.vrs_gps_data_file
    lidar_2D_back_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.lidar_2D_back_stamp_file
    lidar_2D_middle_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.lidar_2D_middle_stamp_file
    lidar_3D_left_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.lidar_3D_left_stamp_file
    lidar_3D_right_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.lidar_3D_right_stamp_file
    stereo_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.stereo_stamp_file

    binary_file_extension: str = ".bin"
    image_file_extension: str = ".png"


encoder = SensorNamePath("encoder", DatasetStructure.encoder_data_file)

# data_stamp.csv file content. The order of the measurements.
data_stamp = [[1, encoder.name]]

# raw measurements
z_encoder_1 = (1, 1.0, 1.0, 1.0)

el1 = Element(
    timestamp=z_encoder_1[0],
    measurement=Measurement(
        sensor=Encoder(encoder.name, params),
        values=tuple(str(i) for i in z_encoder_1[1:]),
    ),
    location=CsvDataLocation(file=encoder.file_path, position=0),
)
