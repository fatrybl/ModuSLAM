from dataclasses import dataclass, field
from pathlib import Path
from configs.system.data_manager.data_manager import DataManagerConfig

from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)

from configs.paths.kaist_dataset import KaistDatasetPathConfig as KaistPaths
from configs.system.data_manager.batch_factory.datasets.base_dataset import DatasetConfig
from configs.system.data_manager.batch_factory.memory import MemoryAnalyzerConfig
from configs.system.data_manager.batch_factory.regime import TimeLimitConfig, StreamConfig
from configs.system.setup_manager.sensor_factory import SensorConfig, SensorFactoryConfig
from configs.system.setup_manager.setup_manager import SetupManagerConfig
from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig, RegimeConfig
from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig, PairConfig

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


dataset_directory: Path = Path("/home/oem/Downloads/urban19-highway/")


iterable_data_files: list[PairConfig] = field(default_factory=lambda: [
    PairConfig(imu.name, dataset_directory / KaistPaths.imu_data_file),
    PairConfig(fog.name, dataset_directory / KaistPaths.fog_data_file),
    PairConfig(encoder.name, dataset_directory / KaistPaths.encoder_data_file),
    PairConfig(altimeter.name, dataset_directory /
               KaistPaths.altimeter_data_file),
    PairConfig(gps.name, dataset_directory / KaistPaths.gps_data_file),
    PairConfig(vrs_gps.name, dataset_directory / KaistPaths.vrs_gps_data_file),
    PairConfig(stereo.name, dataset_directory / KaistPaths.stereo_stamp_file),
    PairConfig(lidar_2D_back.name, dataset_directory /
               KaistPaths.lidar_2D_back_stamp_file),
    PairConfig(lidar_2D_middle.name, dataset_directory /
               KaistPaths.lidar_2D_middle_stamp_file),
    PairConfig(lidar_3D_left.name, dataset_directory /
               KaistPaths.lidar_3D_left_stamp_file),
    PairConfig(lidar_3D_right.name, dataset_directory /
               KaistPaths.lidar_3D_right_stamp_file),
])

data_dirs: list[PairConfig] = field(default_factory=lambda: [
    PairConfig(stereo.name,
               dataset_directory / KaistPaths.image_data_dir),
    PairConfig(lidar_2D_back.name,
               dataset_directory / KaistPaths.lidar_2D_back_dir),
    PairConfig(lidar_2D_middle.name,
               dataset_directory / KaistPaths.lidar_2D_middle_dir),
    PairConfig(lidar_3D_left.name,
               dataset_directory / KaistPaths.lidar_3D_left_dir),
    PairConfig(lidar_3D_right.name,
               dataset_directory / KaistPaths.lidar_3D_right_dir),
])


@dataclass
class KaistDS(KaistConfig):
    directory: Path = dataset_directory
    iterable_data_files: list[PairConfig] = iterable_data_files
    data_dirs: list[PairConfig] = data_dirs


@dataclass
class Memory(MemoryAnalyzerConfig):
    graph_memory: float = 15.0


@dataclass
class TLimit(TimeLimitConfig):
    start: int = 1544578682416523355
    stop: int = 1544578682426144851


@dataclass
class SF(SensorFactoryConfig):
    all_sensors: list[SensorConfig] = all_sensors
    used_sensors: list[SensorConfig] = used_sensors


@dataclass
class SM(SetupManagerConfig):
    sensor_factory: SensorFactoryConfig = field(default_factory=SF)


@dataclass
class BF(BatchFactoryConfig):
    dataset: DatasetConfig = field(default_factory=KaistDS)
    memory: MemoryAnalyzerConfig = field(default_factory=Memory)
    regime: RegimeConfig = field(default_factory=TLimit)


@dataclass
class DM(DataManagerConfig):
    batch_factory: BatchFactoryConfig = field(default_factory=BF)


@dataclass
class Config:
    setup_manager: SetupManagerConfig = field(default_factory=SM)
    data_manager: DataManagerConfig = field(default_factory=DM)
