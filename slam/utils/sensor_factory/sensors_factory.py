import logging

from typing import Type
from pathlib import Path

from slam.utils.config import Config
from slam.utils.exceptions import NotSubset
from slam.utils.meta_singleton import MetaSingleton
from slam.utils.sensor_factory.sensors import Sensor, Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths as paths

logger = logging.getLogger(__name__)


class SensorFactory(metaclass=MetaSingleton):
    def __init__(self):
        self.sensors: set[Type[Sensor]] = set()
        cfg = Config.from_file(paths.data_manager_config.value)
        self.attributes: dict[str, str] = cfg.attributes['sensors']
        self._init_sesnors()
        self._check_used_sesnors()

    def _init_sesnors(self) -> None:
        for item in self.attributes.items():
            sensor = self._map_item_to_sesnor(item)
            self.sensors.add(sensor)

    def _check_used_sesnors(self) -> None:
        cfg = Config.from_file(paths.data_reader_config.value)
        used_sensors: set[str] = set(cfg.attributes['used_sensors'])
        all_sensors: set[str] = set(s.name for s in self.sensors)
        print(used_sensors)
        print(all_sensors)
        if not used_sensors.issubset(all_sensors):
            logger.critical(
                f'some of used sesnor: {used_sensors} is not a part of known sensors: {self.sensors}')
            raise NotSubset

    def name_to_sensor(self, name: str) -> Type[Sensor]:
        for s in self.sensors:
            if s.name == name:
                return s

    def _map_item_to_sesnor(self, item: tuple[str, dict[str, str]]) -> Type[Sensor]:
        name, params = item
        config_file: Path = paths.sensors_config_dir.value / params['config']
        sensor_type = params['type']

        if sensor_type == 'imu':
            return Imu(name, config_file)

        if sensor_type == 'fog':
            return Fog(name, config_file)

        if sensor_type == 'altimeter':
            return Altimeter(name, config_file)

        if sensor_type == 'lidar_2D':
            return Lidar2D(name, config_file)

        if sensor_type == 'lidar_3D':
            return Lidar3D(name, config_file)

        if sensor_type == 'encoder':
            return Encoder(name, config_file)

        if sensor_type == 'stereo_camera':
            return StereoCamera(name, config_file)

        if sensor_type == 'gps':
            return Gps(name, config_file)

        if sensor_type == 'vrs_gps':
            return VrsGps(name, config_file)

        else:
            logger.error(f'unsupported sensor type: {sensor_type}')
            raise KeyError
