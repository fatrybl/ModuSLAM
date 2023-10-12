from dataclasses import dataclass, field
from pathlib import Path
from omegaconf import MISSING
from enum import Enum

from configs.system.setup_manager.setup import SensorConfig, SetupManager
from configs.system.data_manager.manager import DataManager
from configs.system.data_manager.memory import MemoryAnalyzer
from configs.system.data_manager.datasets.base_dataset import Dataset
from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)


class RosDatasetStructure(Enum):
    master_filename = "MasterFilename.txt"
    data_files_folder = Path("dataset1")

@dataclass
class RosSensorConfig(SensorConfig):
    topic: str = MISSING


imu = RosSensorConfig('xsens_imu', Imu.__name__, 'imu.yaml', '/sensors/imu/')
fog = RosSensorConfig('fog', Fog.__name__, 'fog.yaml', '/sensors/fog')
encoder = RosSensorConfig('encoder_1', Encoder.__name__,
                          'encoder.yaml', '/sensors/encoder')
altimeter = RosSensorConfig(
    'altimeter', Altimeter.__name__, 'altimeter.yaml', '/sensors/altimeter')
gps = RosSensorConfig('gps', Gps.__name__, 'gps.yaml', '/sensors/gps')
vrs_gps = RosSensorConfig(
    'vrs_gps', VrsGps.__name__, 'vrs_gps.yaml', '/sensors/vrs_gps')
stereo = RosSensorConfig(
    'realsense_stereo', StereoCamera.__name__, 'stereo.yaml', '/sensors/stereo')
lidar_3D_right = RosSensorConfig(
    'vlp32_right', Lidar3D.__name__, 'velodyne_right.yaml', '/sensors/vlp32_right')
lidar_3D_left = RosSensorConfig(
    'vlp32_left', Lidar3D.__name__, 'velodyne_left.yaml', '/sensors/vlp32_left')
lidar_2D_back = RosSensorConfig(
    'sick_back', Lidar2D.__name__, 'sick_back.yaml', '/sensors/sick_back')
lidar_2D_middle = RosSensorConfig(
    'sick_middle', Lidar2D.__name__, 'sick_middle.yaml', '/sensors/sick_middle')


@dataclass
class Sensors(SetupManager):
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
        default_factory=lambda: [imu, stereo])
    
    sensor_config_dir: Path = field(default_factory=lambda: Path("/home/ilia/mySLAM/configs/sensors"))

@dataclass
class Ros1DS(Dataset):
    type: str = 'ros1'
    directory: Path = Path("/home/oem/Downloads/urban18-highway/")
    time_limit: list[int] = field(default_factory=lambda: [0, 300])
    deserialize_raw_data: bool  = False
    dataset_type: str = 'ros1'
    
@dataclass
class Memory(MemoryAnalyzer):
    graph_memory: float = 30.0


@dataclass
class Ros1DM(DataManager):
    dataset: Ros1DS = field(default_factory=Ros1DS)
    memory: MemoryAnalyzer = field(default_factory=Memory)

@dataclass
class Ros1:
    setup_manager: SetupManager = field(default_factory=Sensors)
    data_manager: DataManager = field(default_factory=Ros1DM)
