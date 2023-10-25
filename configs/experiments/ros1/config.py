from dataclasses import dataclass, field
from pathlib import Path
from omegaconf import MISSING
from enum import Enum

from configs.system.setup_manager.setup import SensorConfig, SetupManager
from configs.system.data_manager.manager import DataManager, Regime, TimeLimit
from configs.system.data_manager.memory import MemoryAnalyzer
from configs.system.data_manager.datasets.base_dataset import Dataset
from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)
from configs.system.data_manager.datasets.ros1 import Ros1

class RosDatasetStructure(Enum):
    master_filename = "MasterFilename.txt"
    data_files_folder = Path("dataset1")

@dataclass
class RosSensorConfig(SensorConfig):
    topic: str = MISSING

imu = RosSensorConfig('xsens_imu', Imu.__name__, 'imu.yaml', '/imu_data')

gps = RosSensorConfig('gps', Gps.__name__, 'gps.yaml', '/position_gps')

stereo = RosSensorConfig(
    'realsense_stereo', StereoCamera.__name__, 'stereo.yaml', "/camera")

lidar_2D_middle = RosSensorConfig(
    'sick_middle', Lidar2D.__name__, 'sick_middle.yaml', '/scan')


used_sensors: list[SensorConfig] = [imu, gps, lidar_2D_middle]

@dataclass
class Sensors(SetupManager):
    all_sensors: list[SensorConfig] = field(
        default_factory=lambda: [
            imu,
            gps,
            lidar_2D_middle,
            stereo
        ])

    used_sensors: list[SensorConfig] = field(
        default_factory=lambda: used_sensors)
    
    sensor_config_dir: Path = field(default_factory=lambda: Path("/home/ilia/mySLAM/configs/sensors"))


@dataclass
class Ros1DS(Ros1):
    deserialize_raw_data: bool  = True
    used_sensors: list[SensorConfig] = field(default_factory=lambda: used_sensors)
    directory: str = field(default_factory=lambda: "/home/ilia/mySLAM/data/rosbag")

@dataclass
class Memory(MemoryAnalyzer):
    graph_memory: float = 40.0

@dataclass
class Range(TimeLimit):
    start: int = 1544578498418802396
    stop: int = 1544578498428802229


@dataclass
class Ros1DM(DataManager):
    dataset: Ros1DS = field(default_factory=Ros1DS)
    memory: MemoryAnalyzer = field(default_factory=Memory)
    regime: Regime = field(default_factory=Range)
    
@dataclass
class Ros1:
    setup_manager: SetupManager = field(default_factory=Sensors)
    data_manager: DataManager = field(default_factory=Ros1DM)
