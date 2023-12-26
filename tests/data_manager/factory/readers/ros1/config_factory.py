from dataclasses import dataclass, field
from pathlib import Path
from omegaconf import MISSING
from enum import Enum

from configs.system.setup_manager.setup_manager import SetupManager
from configs.system.data_manager.data_manager import DataManager
from configs.system.data_manager.memory import MemoryAnalyzer
from configs.system.data_manager.datasets.base_dataset import Dataset
from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)
from configs.system.data_manager.datasets.ros1 import Ros1, RosSensorConfig
from configs.system.data_manager.regime import Regime, TimeLimit,  Stream
from configs.system.setup_manager.sensor_factory import Sensor, SensorFactory

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

class RosDatasetStructure(Enum):
    master_filename = "MasterFilename.txt"
    data_files_folder = Path("dataset1")

imu = Sensor('imu', Imu.__name__, ImuParameter())
fog = Sensor('fog', Fog.__name__, FogParameter())
encoder = Sensor('encoder', Encoder.__name__, EncoderParameter())
altimeter = Sensor('altimeter', Altimeter.__name__, AltimeterParameter())
gps = Sensor('gps', Gps.__name__, GpsParameter())
vrs_gps = Sensor('vrs', VrsGps.__name__, VrsGpsParameter())
stereo = Sensor('stereo', StereoCamera.__name__, StereoParameter())
lidar_3D_right = Sensor(
    'velodyne_right', Lidar3D.__name__, VelodyneLeftParameter())
lidar_3D_left = Sensor('velodyne_left', Lidar3D.__name__,
                       VelodyneRightParameter())
lidar_2D_back = Sensor(
    'sick_back', Lidar2D.__name__, SickBackParameter())
lidar_2D_middle = Sensor(
    'sick_middle', Lidar2D.__name__, SickMiddleParameter())


all_sensors: list[Sensor] = field(
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

used_sensors: list[Sensor] = field(
    default_factory=lambda: [imu,
                             gps,
                             lidar_2D_middle
                             ])


@dataclass
class SF(SensorFactory):
    all_sensors: list[Sensor] = all_sensors
    used_sensors: list[Sensor] = used_sensors


@dataclass
class SM(SetupManager):
    sensor_factory: SensorFactory = field(default_factory=SF)


imu_ros = RosSensorConfig(imu, '/imu_topic')

gps_ros = RosSensorConfig(gps, '/gps_topic')

stereo_ros = RosSensorConfig(stereo, "/camera_topic")

lidar_2D_middle_ros = RosSensorConfig(lidar_2D_middle, '/scan_topic')

      
@dataclass
class Ros1DS(Ros1):
    deserialize_raw_data: bool = False
    used_sensors: list[RosSensorConfig] = field(default_factory= lambda: [imu_ros, gps_ros, lidar_2D_middle_ros, stereo_ros])
    directory: str = field(default_factory=lambda: Path(__file__).parent)

@dataclass
class Memory(MemoryAnalyzer):
    graph_memory: float = 40.0

@dataclass
class Range(TimeLimit):
    start: int = 1544578498418802396
    stop: int = 1544578498428802229


@dataclass
class Ros1DM(DataManager):
    regime: Regime = field(default_factory=Stream)
    dataset: Dataset = field(default_factory=Ros1DS)
    memory: MemoryAnalyzer = field(default_factory=Memory)
    
@dataclass
class ConfigRos1:
    setup_manager: SetupManager = field(default_factory=SM)
    data_manager: DataManager = field(default_factory=Ros1DM)

