from dataclasses import dataclass, field
from pathlib import Path

from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)


from configs.experiments.kaist.config import Memory
from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig
from configs.system.data_manager.batch_factory.datasets.base_dataset import DatasetConfig
from configs.system.data_manager.batch_factory.memory import MemoryAnalyzerConfig
from configs.system.data_manager.batch_factory.regime import RegimeConfig, StreamConfig
from configs.paths.kaist_dataset import KaistDatasetPathConfig as KaistPaths
from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig, PairConfig
from configs.system.setup_manager.sensor_factory import SensorConfig
from configs.sensors.base_sensor_parameters import ParameterConfig


DATASET_DIR: Path = Path(__file__).parent / 'test_data'


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

iterable_data_files: list[PairConfig] = field(default_factory=lambda: [
    PairConfig(imu.name, DATASET_DIR / KaistPaths.imu_data_file),
    PairConfig(fog.name, DATASET_DIR / KaistPaths.fog_data_file),
    PairConfig(encoder.name, DATASET_DIR / KaistPaths.encoder_data_file),
    PairConfig(altimeter.name, DATASET_DIR / KaistPaths.altimeter_data_file),
    PairConfig(gps.name, DATASET_DIR / KaistPaths.gps_data_file),
    PairConfig(vrs_gps.name, DATASET_DIR / KaistPaths.vrs_gps_data_file),
    PairConfig(stereo.name, DATASET_DIR / KaistPaths.stereo_stamp_file),
    PairConfig(lidar_2D_back.name, DATASET_DIR /
               KaistPaths.lidar_2D_back_stamp_file),
    PairConfig(lidar_2D_middle.name, DATASET_DIR /
               KaistPaths.lidar_2D_middle_stamp_file),
    PairConfig(lidar_3D_left.name, DATASET_DIR /
               KaistPaths.lidar_3D_left_stamp_file),
    PairConfig(lidar_3D_right.name, DATASET_DIR /
               KaistPaths.lidar_3D_right_stamp_file),
])

data_dirs: list[PairConfig] = field(default_factory=lambda: [
    PairConfig(stereo.name, DATASET_DIR / KaistPaths.image_data_dir),
    PairConfig(lidar_2D_back.name, DATASET_DIR / KaistPaths.lidar_2D_back_dir),
    PairConfig(lidar_2D_middle.name, DATASET_DIR /
               KaistPaths.lidar_2D_middle_dir),
    PairConfig(lidar_3D_left.name, DATASET_DIR / KaistPaths.lidar_3D_left_dir),
    PairConfig(lidar_3D_right.name, DATASET_DIR /
               KaistPaths.lidar_3D_right_dir),
])


@dataclass
class KaistReaderConfig(KaistConfig):
    directory: Path = DATASET_DIR
    iterable_data_files: list[PairConfig] = iterable_data_files
    data_dirs: list[PairConfig] = data_dirs


@dataclass
class BFConfig(BatchFactoryConfig):
    regime: RegimeConfig = field(default_factory=StreamConfig)
    dataset: DatasetConfig = field(default_factory=KaistReaderConfig)
    memory: MemoryAnalyzerConfig = field(default_factory=Memory)
