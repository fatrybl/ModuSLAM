import logging

from typing import Type
from pathlib import Path

from slam.utils.exceptions import NotSubset, SensorNotFound
from slam.utils.meta_singleton import MetaSingleton
from configs.system.setup_manager.setup import SensorConfig, SetupManager as SetupManagerConfig
from slam.setup_manager.sensor_factory.sensors import (
    Sensor, Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)

logger = logging.getLogger(__name__)


class SensorFactory(metaclass=MetaSingleton):
    """Factory class for sensors management. Defaults to MetaSingleton.

    Class Attributes: 
        all_sensors: sensors to be used in experiments for a particluar dataset.
        used_sensors: sensors to be used in the experiment for a particluar dataset. Must be a subset of all_sensors.

    Raises:
        SensorNotFound: there is no sensor with the requested sensor name among all sensors.
        NotSubset: some of used sensor are not defined in all sensors set.
        ValueError: there is no available sensor type for the item from config.
    """

    all_sensors: set[Type[Sensor]] = set()
    used_sensors: set[Type[Sensor]] = set()

    def __init__(self, cfg: SetupManagerConfig):
        self.__all_sensors_list: list[SensorConfig] = cfg.all_sensors
        self.__used_sensors_list: list[SensorConfig] = cfg.used_sensors
        self.__sensor_config_dir: Path = cfg.sensor_config_dir
        self._init_sesnors()
        self._check_used_sesnors()

    @classmethod
    def get_used_sensors(cls) -> set[Type[Sensor]]:
        return cls.used_sensors

    @classmethod
    def get_all_sensors(cls) -> set[Type[Sensor]]:
        return cls.all_sensors

    @classmethod
    def name_to_sensor(cls, name: str) -> Type[Sensor]:
        """Maps sensor name to Sensor (if exists) and returns the corresponding sensor.

        Args:
            name (str): sensor name

        Raises:
            SensorNotFound: there is no sensor with the requested sensor name among all sensors.

        Returns:
            Type[Sensor]: sensor if it exists among all sensors.
        """
        for s in cls.all_sensors:
            if s.name == name:
                sensor = s
                return sensor

        msg = f"No sensor with name {name} in {cls.all_sensors}"
        logger.critical(msg)
        raise SensorNotFound


    def _init_sesnors(self) -> None:
        """Initializes all sensors and used sensors from config."""
        for s in self.__all_sensors_list:
            sensor = self._map_item_to_sesnor(s)
            self.all_sensors.add(sensor)

        for s in self.__used_sensors_list:
            sensor = self.name_to_sensor(s.name)
            self.used_sensors.add(sensor)

    def _check_used_sesnors(self) -> None:
        """Checks if used sensors are part of all initialized sensors.

        Raises:
            NotSubset: Some of used sensor are not defined in all sensors set.
        """
        if not self.used_sensors or not self.used_sensors.issubset(self.all_sensors):
            msg = f'Used sensors: {self.used_sensors} are not in known sensors: {self.all_sensors} or empty'
            logger.critical(msg)
            raise NotSubset(msg)

    def _map_item_to_sesnor(self, item: SensorConfig) -> Type[Sensor]:
        """ Creates sensor from config item.

        Args:
            item (SensorConfig): item from config

        Raises:
            ValueError: there is no available sensor type for the item from config.
        Returns:
            Type[Sensor]: sensor
        """
        name: str = item.name
        sensor_type: str = item.type
        config_file: Path = self.__sensor_config_dir / item.config_name

        if sensor_type == Imu.__name__:
            return Imu(name, config_file)

        elif sensor_type == Fog.__name__:
            return Fog(name, config_file)

        elif sensor_type == Altimeter.__name__:
            return Altimeter(name, config_file)

        elif sensor_type == Lidar2D.__name__:
            return Lidar2D(name, config_file)

        elif sensor_type == Lidar3D.__name__:
            return Lidar3D(name, config_file)

        elif sensor_type == Encoder.__name__:
            return Encoder(name, config_file)

        elif sensor_type == StereoCamera.__name__:
            return StereoCamera(name, config_file)

        elif sensor_type == Gps.__name__:
            return Gps(name, config_file)

        elif sensor_type == VrsGps.__name__:
            return VrsGps(name, config_file)

        else:
            msg = f'unsupported sensor type: {sensor_type}'
            logger.error(msg)
            raise ValueError(msg)
