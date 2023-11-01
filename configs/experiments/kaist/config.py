from dataclasses import dataclass, field
from pathlib import Path

from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)

from configs.paths.kaist_dataset import KaistDatasetPath as KaistPaths
from configs.system.data_manager.datasets.base_dataset import DatasetConfig
from configs.system.data_manager.memory import MemoryAnalyzer
from configs.system.data_manager.regime import TimeLimit, Stream
from configs.system.setup_manager.sensor_factory import SensorConfig, SensorFactoryConfig
from configs.system.setup_manager.setup_manager import SetupManager
from configs.system.data_manager.data_manager import DataManager, Regime
from configs.system.data_manager.datasets.kaist import KaistConfig, Pair

from configs.sensors.imu import ImuParameter
from configs.sensors.fog import FogParameter
from configs.sensors.encoder import EncoderParameter
from configs.sensors.altimeter import AltimeterParameter
from configs.sensors.gps import GpsParameter
from configs.sensors.sick_back import SickBackParameter
from configs.sensors.sick_middle import SickMiddleParameter
from configs.sensors.stereo import StereoParameter
from configs.sensors.velodyne_left import VelodyneLeftParameter
from configs.sensors.velodyne_right import VelodyneRightParameter
from configs.sensors.vrs_gps import VrsGpsParameter


imu = SensorConfig('imu', Imu.__name__, ImuParameter())
fog = SensorConfig('fog', Fog.__name__, FogParameter())
encoder = SensorConfig('encoder', Encoder.__name__, EncoderParameter())
altimeter = SensorConfig('altimeter', Altimeter.__name__, AltimeterParameter())
gps = SensorConfig('gps', Gps.__name__, GpsParameter())
vrs_gps = SensorConfig('vrs', VrsGps.__name__, VrsGpsParameter())
stereo = SensorConfig('stereo', StereoCamera.__name__, StereoParameter())
lidar_3D_right = SensorConfig(
    'velodyne_right', Lidar3D.__name__, VelodyneLeftParameter())
lidar_3D_left = SensorConfig('velodyne_left', Lidar3D.__name__,
                             VelodyneRightParameter())
lidar_2D_back = SensorConfig(
    'sick_back', Lidar2D.__name__, SickBackParameter())
lidar_2D_middle = SensorConfig(
    'sick_middle', Lidar2D.__name__, SickMiddleParameter())


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
    Pair(stereo.name,
         dataset_directory / KaistPaths.image_data_dir),
    Pair(lidar_2D_back.name,
         dataset_directory / KaistPaths.lidar_2D_back_dir),
    Pair(lidar_2D_middle.name,
         dataset_directory / KaistPaths.lidar_2D_middle_dir),
    Pair(lidar_3D_left.name,
         dataset_directory / KaistPaths.lidar_3D_left_dir),
    Pair(lidar_3D_right.name,
         dataset_directory / KaistPaths.lidar_3D_right_dir),
])


@dataclass
class KaistDS(KaistConfig):
    directory: Path = dataset_directory
    iterable_data_files: list[Pair] = iterable_data_files
    data_dirs: list[Pair] = data_dirs


@dataclass
class Memory(MemoryAnalyzer):
    graph_memory: float = 30.0


@dataclass
class Range(TimeLimit):
    start: int = 1544578498418802396
    stop: int = 1544578498428802229


@dataclass
class SF(SensorFactoryConfig):
    all_sensors: list[SensorConfig] = all_sensors
    used_sensors: list[SensorConfig] = used_sensors


@dataclass
class SM(SetupManager):
    sensor_factory: SensorFactoryConfig = field(default_factory=SF)


@dataclass
class DM(DataManager):
    dataset: DatasetConfig = field(default_factory=KaistDS)
    memory: MemoryAnalyzer = field(default_factory=Memory)
    regime: Regime = field(default_factory=Stream)


@dataclass
class Config:
    setup_manager: SetupManager = field(default_factory=SM)
    data_manager: DataManager = field(default_factory=DM)
