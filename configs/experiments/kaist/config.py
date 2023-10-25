from dataclasses import dataclass, field
from pathlib import Path

from configs.paths.default import ConfigPaths
from configs.paths.kaist_dataset import KaistDataset as KaistPaths
from configs.system.data_manager.datasets.base_dataset import Dataset
from configs.system.data_manager.memory import MemoryAnalyzer
from configs.system.setup_manager.setup import SensorConfig, SetupManager
from configs.system.data_manager.manager import DataManager, Regime, Stream, TimeLimit
from configs.system.data_manager.datasets.kaist import Kaist, Pair
from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)


imu = SensorConfig('imu', Imu.__name__, 'imu.yaml')
fog = SensorConfig('fog', Fog.__name__, 'fog.yaml')
encoder = SensorConfig('encoder', Encoder.__name__, 'encoder.yaml')
altimeter = SensorConfig('altimeter', Altimeter.__name__, 'altimeter.yaml')
gps = SensorConfig('gps', Gps.__name__, 'gps.yaml')
vrs_gps = SensorConfig('vrs', VrsGps.__name__, 'vrs_gps.yaml')
stereo = SensorConfig('stereo', StereoCamera.__name__, 'stereo.yaml')
lidar_3D_right = SensorConfig(
    'velodyne_right', Lidar3D.__name__, 'velodyne_right.yaml')
lidar_3D_left = SensorConfig(
    'velodyne_left', Lidar3D.__name__, 'velodyne_left.yaml')
lidar_2D_back = SensorConfig(
    'sick_back', Lidar2D.__name__, 'sick_back.yaml')
lidar_2D_middle = SensorConfig(
    'sick_middle', Lidar2D.__name__, 'sick_middle.yaml')


all_sensors: list[SensorConfig] = field(
    default_factory=lambda: [
        imu,
        fog,
        encoder,
        stereo,
        altimeter,
        gps,
        vrs_gps,
        lidar_3D_right,
        lidar_3D_left,
        lidar_2D_middle,
        lidar_2D_back
    ])

used_sensors: list[SensorConfig] = field(
    default_factory=lambda: [imu,
                             fog,
                             encoder,
                             stereo,
                             altimeter,
                             gps,
                             vrs_gps,
                             lidar_3D_right,
                             lidar_3D_left,
                             lidar_2D_middle,
                             lidar_2D_back])

sensor_config_dir: Path = ConfigPaths.sensors_config_dir


dataset_directory: Path = Path("/home/oem/Downloads/urban18-highway/")


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
class KaistDS(Kaist):
    data_stamp_file: Path = dataset_directory / KaistPaths.data_stamp
    directory: Path = dataset_directory
    iterable_data_files: list[Pair] = iterable_data_files
    data_dirs: list[Pair] = data_dirs


@dataclass
class Memory(MemoryAnalyzer):
    graph_memory: float = 30.0


@dataclass
class SM(SetupManager):
    all_sensors: list[SensorConfig] = all_sensors
    used_sensors: list[SensorConfig] = used_sensors
    sensor_config_dir: Path = sensor_config_dir


@dataclass
class Range(TimeLimit):
    start: int = 1544578498418802396
    stop: int = 1544578498428802229


@dataclass
class DM(DataManager):
    dataset: Dataset = field(default_factory=KaistDS)
    memory: MemoryAnalyzer = field(default_factory=Memory)
    regime: Regime = field(default_factory=Stream)


@dataclass
class Config:
    setup_manager: SetupManager = field(default_factory=SM)
    data_manager: DataManager = field(default_factory=DM)
