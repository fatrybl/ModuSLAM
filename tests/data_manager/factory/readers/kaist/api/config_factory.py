from dataclasses import dataclass, field
from pathlib import Path


from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)

from configs.paths.kaist_dataset import KaistDatasetPath as KaistPaths
from configs.system.data_manager.datasets.kaist import Kaist, Pair
from configs.system.setup_manager.sensor_factory import Sensor, SensorFactory
from configs.sensors.base_sensor_parameters import Parameter

from .data_factory import DataFactory


class ImuParameter(Parameter):
    "some parameters"


class FogParameter(Parameter):
    "some parameters"


class EncoderParameter(Parameter):
    "some parameters"


class AltimeterParameter(Parameter):
    "some parameters"


class GpsParameter(Parameter):
    "some parameters"


class VrsGpsParameter(Parameter):
    "some parameters"


class StereoParameter(Parameter):
    "some parameters"


class VelodyneLeftParameter(Parameter):
    "some parameters"


class VelodyneRightParameter(Parameter):
    "some parameters"


class SickBackParameter(Parameter):
    "some parameters"


class SickMiddleParameter(Parameter):
    "some parameters"


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
                             lidar_2D_back
                             ])

used_sensors: list[Sensor] = field(
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

dataset_directory: Path = DataFactory.TEST_DATA_DIR

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
class SensorFactoryConfig(SensorFactory):
    all_sensors: list[Sensor] = all_sensors
    used_sensors: list[Sensor] = used_sensors


@dataclass
class KaistReaderConfig(Kaist):
    directory: Path = DataFactory.TEST_DATA_DIR
    iterable_data_files: list[Pair] = iterable_data_files
    data_dirs: list[Pair] = data_dirs
