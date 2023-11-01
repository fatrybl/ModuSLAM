from dataclasses import dataclass, field
from pathlib import Path


from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)

from configs.paths.kaist_dataset import KaistDatasetPath as KaistPaths
from configs.system.data_manager.datasets.kaist import KaistConfig, Pair
from configs.system.setup_manager.sensor_factory import SensorConfig
from configs.sensors.base_sensor_parameters import ParameterConfig

from api.data_factory import DatasetStructure

DATASET_DIR: Path = DatasetStructure.DATASET_DIR


imu = SensorConfig('imu', Imu.__name__, ParameterConfig())
fog = SensorConfig('fog', Fog.__name__, ParameterConfig())
encoder = SensorConfig('encoder', Encoder.__name__, ParameterConfig())
altimeter = SensorConfig('altimeter', Altimeter.__name__, ParameterConfig())
gps = SensorConfig('gps', Gps.__name__, ParameterConfig())
vrs_gps = SensorConfig('vrs', VrsGps.__name__, ParameterConfig())
stereo = SensorConfig('stereo', StereoCamera.__name__, ParameterConfig())
lidar_3D_right = SensorConfig(
    'velodyne_right', Lidar3D.__name__, ParameterConfig())
lidar_3D_left = SensorConfig(
    'velodyne_left', Lidar3D.__name__, ParameterConfig())
lidar_2D_back = SensorConfig(
    'sick_back', Lidar2D.__name__, ParameterConfig())
lidar_2D_middle = SensorConfig(
    'sick_middle', Lidar2D.__name__, ParameterConfig())

iterable_data_files: list[Pair] = field(default_factory=lambda: [
    Pair(imu.name, DATASET_DIR / KaistPaths.imu_data_file),
    Pair(fog.name, DATASET_DIR / KaistPaths.fog_data_file),
    Pair(encoder.name, DATASET_DIR / KaistPaths.encoder_data_file),
    Pair(altimeter.name, DATASET_DIR / KaistPaths.altimeter_data_file),
    Pair(gps.name, DATASET_DIR / KaistPaths.gps_data_file),
    Pair(vrs_gps.name, DATASET_DIR / KaistPaths.vrs_gps_data_file),
    Pair(stereo.name, DATASET_DIR / KaistPaths.stereo_stamp_file),
    Pair(lidar_2D_back.name, DATASET_DIR /
         KaistPaths.lidar_2D_back_stamp_file),
    Pair(lidar_2D_middle.name, DATASET_DIR /
         KaistPaths.lidar_2D_middle_stamp_file),
    Pair(lidar_3D_left.name, DATASET_DIR /
         KaistPaths.lidar_3D_left_stamp_file),
    Pair(lidar_3D_right.name, DATASET_DIR /
         KaistPaths.lidar_3D_right_stamp_file),
])

data_dirs: list[Pair] = field(default_factory=lambda: [
    Pair(stereo.name, DATASET_DIR / KaistPaths.image_data_dir),
    Pair(lidar_2D_back.name, DATASET_DIR / KaistPaths.lidar_2D_back_dir),
    Pair(lidar_2D_middle.name, DATASET_DIR /
         KaistPaths.lidar_2D_middle_dir),
    Pair(lidar_3D_left.name, DATASET_DIR / KaistPaths.lidar_3D_left_dir),
    Pair(lidar_3D_right.name, DATASET_DIR / KaistPaths.lidar_3D_right_dir),
])


@dataclass
class KaistReaderConfig(KaistConfig):
    directory: Path = DATASET_DIR
    iterable_data_files: list[Pair] = iterable_data_files
    data_dirs: list[Pair] = data_dirs
