import logging

from typing import Type
from configs.sensors.base_sensor_parameters import ParameterConfig

from slam.utils.exceptions import NotSubset, SensorNotFound
from slam.utils.meta_singleton import MetaSingleton
from slam.setup_manager.sensor_factory.sensors import (
    Sensor, Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)

from configs.system.setup_manager.sensor_factory import SensorFactoryConfig as Config
from configs.system.setup_manager.sensor_factory import Sensor as SensorConfig

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

    def __init__(self, cfg: Config):
        self.__all_sensors_list: list[SensorConfig] = cfg.all_sensors
        self.__used_sensors_list: list[SensorConfig] = cfg.used_sensors
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
        raise SensorNotFound(msg)

    def _init_sesnors(self) -> None:
        """Initializes all sensors and used sensors from config."""
        for s in self.__all_sensors_list:
            sensor = self.sensor_from_config(s)
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

    @staticmethod
    def sensor_from_config(cfg: SensorConfig) -> Type[Sensor]:
        """ Creates sensor from config item.
        Args:
            item (SensorConfig): item from config

        Raises:
            ValueError: there is no available sensor type for the item from config.
        Returns:
            Type[Sensor]: sensor
        """
        name: str = cfg.name
        sensor_type: str = cfg.type
        params: Type[ParameterConfig] = cfg.config

        if sensor_type == Imu.__name__:
            return Imu(name, params)

        elif sensor_type == Fog.__name__:
            return Fog(name, params)

        elif sensor_type == Altimeter.__name__:
            return Altimeter(name, params)

        elif sensor_type == Lidar2D.__name__:
            return Lidar2D(name, params)

        elif sensor_type == Lidar3D.__name__:
            return Lidar3D(name, params)

        elif sensor_type == Encoder.__name__:
            return Encoder(name, params)

        elif sensor_type == StereoCamera.__name__:
            return StereoCamera(name, params)

        elif sensor_type == Gps.__name__:
            return Gps(name, params)

        elif sensor_type == VrsGps.__name__:
            return VrsGps(name, params)

        else:
            msg = f'unsupported sensor type: {sensor_type}'
            logger.error(msg)
            raise ValueError(msg)
