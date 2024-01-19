import logging
from typing import Type

from configs.sensors.base_sensor_parameters import ParameterConfig
from configs.system.setup_manager.sensor_factory import (
    SensorConfig,
    SensorFactoryConfig,
)
from slam.setup_manager.sensor_factory.sensors import (
    Altimeter,
    Encoder,
    Fog,
    Gps,
    Imu,
    Lidar2D,
    Lidar3D,
    Sensor,
    StereoCamera,
    VrsGps,
)
from slam.utils.exceptions import NotSubset, SensorNotFound

logger = logging.getLogger(__name__)


class SensorFactory:
    """
    Factory class for sensors management.

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

    @classmethod
    def get_used_sensors(cls) -> set[Type[Sensor]]:
        return cls.used_sensors

    @classmethod
    def get_all_sensors(cls) -> set[Type[Sensor]]:
        return cls.all_sensors

    @classmethod
    def name_to_sensor(cls, name: str) -> Type[Sensor]:
        """
        Maps sensor name to Sensor (if exists) and returns the corresponding sensor.

        Args:
            name (str): sensor name

        Raises:
            SensorNotFound: there is no sensor with the requested sensor name among all sensors.

        Returns:
            Type[Sensor]: sensor if it exists among all sensors.
        """
        for s in cls.all_sensors:
            if s.name == name:
                return s

        msg = f"No sensor with name {name} in {cls.all_sensors}"
        logger.critical(msg)
        raise SensorNotFound(msg)

    @classmethod
    def init_sensors(cls, cfg: SensorFactoryConfig) -> None:
        """
        Initializes all sensors and used sensors from config.
        """
        _all_sensors_list: list[SensorConfig] = cfg.all_sensors
        _used_sensors_list: list[SensorConfig] = cfg.used_sensors

        for s in _all_sensors_list:
            sensor = cls.sensor_from_config(s)
            cls.all_sensors.add(sensor)

        for s in _used_sensors_list:
            sensor = cls.name_to_sensor(s.name)
            cls.used_sensors.add(sensor)

        cls._check_used_sesnors()

    @classmethod
    def _check_used_sesnors(cls) -> None:
        """
        Checks if used sensors are part of all initialized sensors.

        Raises:
            NotSubset: Some of used sensor are not defined in all sensors set.
        """
        if not cls.used_sensors or not cls.used_sensors.issubset(cls.all_sensors):
            msg = f"Used sensors: {cls.used_sensors} are not in known sensors: {cls.all_sensors} or empty"
            logger.critical(msg)
            raise NotSubset(msg)

    @staticmethod
    def sensor_from_config(cfg: SensorConfig) -> Type[Sensor]:
        """
        Creates sensor from config item.

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
            msg = f"unsupported sensor type: {sensor_type}"
            logger.error(msg)
            raise ValueError(msg)
