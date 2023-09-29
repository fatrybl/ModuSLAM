from dataclasses import dataclass, field

from configs.paths.DEFAULT_FILE_PATHS import KaistDataset as KaistDatasetPaths
from configs.system.setup_manager.setup import SensorConfig, SetupManager
from configs.system.data_manager.manager import DataManager
from configs.system.data_manager.datasets.kaist import KaistDataset, Pair
from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)


imu = SensorConfig('xsens_imu', Imu.__name__, 'imu.yaml')
fog = SensorConfig('fog', Fog.__name__, 'fog.yaml')
encoder = SensorConfig('encoder_1', Encoder.__name__, 'encoder.yaml')
altimeter = SensorConfig('altimeter', Altimeter.__name__, 'altimeter.yaml')
gps = SensorConfig('gps', Gps.__name__, 'gps.yaml')
vrs_gps = SensorConfig('vrs_gps', VrsGps.__name__, 'vrs_gps.yaml')
stereo = SensorConfig('realsense_stereo', StereoCamera.__name__, 'stereo.yaml')
lidar_3D_right = SensorConfig(
    'vlp32_right', Lidar3D.__name__, 'velodyne_right.yaml')
lidar_3D_left = SensorConfig(
    'vlp32_left', Lidar3D.__name__, 'velodyne_left.yaml')
lidar_2D_back = SensorConfig(
    'sick_back', Lidar2D.__name__, 'sick_back.yaml')
lidar_2D_middle = SensorConfig(
    'sick_middle', Lidar2D.__name__, 'sick_middle.yaml')


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


@dataclass
class KaistDS(KaistDataset):
    type: str = 'kaist'
    directory: str = "/home/oem/Downloads/urban18-highway/"
    data_stamp_file = 'data_stamp.csv'
    sensor_data_location: list[Pair] = field(default_factory=lambda: [
        Pair(imu.name, KaistDatasetPaths.imu_data_file.value),
        Pair(fog.name, KaistDatasetPaths.fog_data_file.value),
        Pair(encoder.name, KaistDatasetPaths.encoder_data_file.value),
        Pair(altimeter.name,
             KaistDatasetPaths.altimeter_data_file.value),
        Pair(gps.name, KaistDatasetPaths.gps_data_file.value),
        Pair(vrs_gps.name, KaistDatasetPaths.vrs_gps_data_file.value),
        Pair(stereo.name, KaistDatasetPaths.image_data_dir.value),
        Pair(lidar_2D_back.name,
             KaistDatasetPaths.lidar_2D_back_dir.value),
        Pair(lidar_2D_middle.name,
             KaistDatasetPaths.lidar_2D_middle_dir.value),
        Pair(lidar_3D_left.name,
             KaistDatasetPaths.lidar_3D_left_dir.value),
        Pair(lidar_3D_right.name,
             KaistDatasetPaths.lidar_3D_right_dir.value),
    ])


@dataclass
class KaistDM(DataManager):
    dataset: KaistDS = field(default_factory=KaistDS)


@dataclass
class Kaist:
    setup_manager: SetupManager = field(default_factory=Sensors)
    data_manager: DataManager = field(default_factory=KaistDM)
