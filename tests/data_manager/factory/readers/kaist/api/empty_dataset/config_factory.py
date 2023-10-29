from dataclasses import dataclass, field
from pathlib import Path


from slam.setup_manager.sensor_factory.sensors import Imu

from configs.paths.kaist_dataset import KaistDatasetPath as KaistPaths
from configs.system.data_manager.datasets.kaist import Kaist, Pair
from configs.system.setup_manager.sensor_factory import Sensor, SensorFactoryConfig
from configs.sensors.base_sensor_parameters import ParameterConfig

from .data_factory import DataFactory


class ImuParameter(ParameterConfig):
    "some parameters"


imu = Sensor('imu', Imu.__name__, ImuParameter())


all_sensors: list[Sensor] = field(
    default_factory=lambda: [imu])

used_sensors: list[Sensor] = field(
    default_factory=lambda: [imu])

dataset_directory: Path = DataFactory.TEST_DATA_DIR

iterable_data_files: list[Pair] = field(default_factory=lambda: [
    Pair(imu.name, dataset_directory / KaistPaths.imu_data_file)
])

data_dirs: list[Pair] = field(default_factory=lambda: [])


@dataclass
class SensorFactoryConfig(SensorFactoryConfig):
    all_sensors: list[Sensor] = all_sensors
    used_sensors: list[Sensor] = used_sensors


@dataclass
class KaistReaderConfig(Kaist):
    directory: Path = DataFactory.TEST_DATA_DIR
    iterable_data_files: list[Pair] = iterable_data_files
    data_dirs: list[Pair] = data_dirs
