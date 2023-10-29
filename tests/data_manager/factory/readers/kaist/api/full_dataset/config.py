from dataclasses import dataclass, field
from pathlib import Path


from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)

from configs.paths.kaist_dataset import KaistDatasetPath as KaistPaths
from configs.system.data_manager.datasets.kaist import Kaist, Pair
from configs.system.setup_manager.sensor_factory import Sensor
from configs.sensors.base_sensor_parameters import ParameterConfig


CURRENT_DIR = Path(__file__).parent
TMP_DIR: Path = CURRENT_DIR / 'tmp'
TEST_DATA_DIR: Path = TMP_DIR / 'test_data'

CONFIG_MODULE_DIR: str = "full_dataset.conf"
DATASET_CONFIG_NAME: str = "dataset_config"
REGIME_CONFIG_NAME: str = "regime_config"
SENSOR_CONFIG_NAME: str = "sensor_factory_config"

dataset_directory: Path = TEST_DATA_DIR


imu = Sensor('imu', Imu.__name__, ParameterConfig())
fog = Sensor('fog', Fog.__name__, ParameterConfig())
encoder = Sensor('encoder', Encoder.__name__, ParameterConfig())
altimeter = Sensor('altimeter', Altimeter.__name__, ParameterConfig())
gps = Sensor('gps', Gps.__name__, ParameterConfig())
vrs_gps = Sensor('vrs', VrsGps.__name__, ParameterConfig())
stereo = Sensor('stereo', StereoCamera.__name__, ParameterConfig())
lidar_3D_right = Sensor(
    'velodyne_right', Lidar3D.__name__, ParameterConfig())
lidar_3D_left = Sensor(
    'velodyne_left', Lidar3D.__name__, ParameterConfig())
lidar_2D_back = Sensor(
    'sick_back', Lidar2D.__name__, ParameterConfig())
lidar_2D_middle = Sensor(
    'sick_middle', Lidar2D.__name__, ParameterConfig())

iterable_data_files: list[Pair] = field(default_factory=lambda: [
    Pair(imu.name, dataset_directory / KaistPaths.imu_data_file),
    Pair(fog.name, dataset_directory / KaistPaths.fog_data_file),
    Pair(encoder.name, dataset_directory / KaistPaths.encoder_data_file),
    Pair(altimeter.name, dataset_directory / KaistPaths.altimeter_data_file),
    Pair(gps.name, dataset_directory / KaistPaths.gps_data_file),
    Pair(vrs_gps.name, dataset_directory / KaistPaths.vrs_gps_data_file),
    Pair(stereo.name, dataset_directory / KaistPaths.stereo_stamp_file),
    Pair(lidar_2D_back.name, dataset_directory /
         KaistPaths.lidar_2D_back_stamp_file),
    Pair(lidar_2D_middle.name, dataset_directory /
         KaistPaths.lidar_2D_middle_stamp_file),
    Pair(lidar_3D_left.name, dataset_directory /
         KaistPaths.lidar_3D_left_stamp_file),
    Pair(lidar_3D_right.name, dataset_directory /
         KaistPaths.lidar_3D_right_stamp_file),
])

data_dirs: list[Pair] = field(default_factory=lambda: [
    Pair(stereo.name, dataset_directory / KaistPaths.image_data_dir),
    Pair(lidar_2D_back.name, dataset_directory / KaistPaths.lidar_2D_back_dir),
    Pair(lidar_2D_middle.name, dataset_directory /
         KaistPaths.lidar_2D_middle_dir),
    Pair(lidar_3D_left.name, dataset_directory / KaistPaths.lidar_3D_left_dir),
    Pair(lidar_3D_right.name, dataset_directory / KaistPaths.lidar_3D_right_dir),
])


@dataclass
class KaistReaderConfig(Kaist):
    directory: Path = dataset_directory
    iterable_data_files: list[Pair] = iterable_data_files
    data_dirs: list[Pair] = data_dirs
