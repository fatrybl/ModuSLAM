import logging

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

    _all_sensors: set[Sensor] = set()
    _used_sensors: set[Sensor] = set()

    @classmethod
    def _check_used_sensors(cls) -> None:
        """
        Checks if used sensors are part of all initialized sensors.

        Raises:
            NotSubset: Some of used sensor are not defined in all sensors set.
        """
        if not cls._used_sensors or not cls._used_sensors.issubset(cls._all_sensors):
            msg = f"Used sensors: {cls._used_sensors} do not present in known sensors: {cls._all_sensors} or empty"
            logger.critical(msg)
            raise NotSubset(msg)

    @classmethod
    def get_used_sensors(cls) -> set[Sensor]:
        """
        Get sensors which have been used in experiment.
        Returns:
            (set[Sensor]): used sensors which have been used in experiment.
        """
        return cls._used_sensors

    @classmethod
    def get_all_sensors(cls) -> set[Sensor]:
        """
        Get all sensors which have been initialized.
        Returns:
            (set[Sensor]): all sensors which have been initialized
        """
        return cls._all_sensors

    @classmethod
    def get_sensor(cls, name: str) -> Sensor:
        """
        Maps sensor name to Sensor (if exists) and returns the corresponding sensor.

        Args:
            name (str): sensor name

        Raises:
            SensorNotFound: there is no sensor with the requested sensor name among all sensors.

        Returns:
            Type[Sensor]: sensor if it exists among all sensors.
        """
        for s in cls._all_sensors:
            if s.name == name:
                return s

        msg = f"No sensor with name {name!r} in {cls._all_sensors}"
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
            cls._all_sensors.add(sensor)

        for s in _used_sensors_list:
            sensor = cls.get_sensor(s.name)
            cls._used_sensors.add(sensor)

        cls._check_used_sensors()

    @staticmethod
    def sensor_from_config(cfg: SensorConfig) -> Sensor:
        """
        Creates sensor from config item.

        Args:
            cfg (SensorConfig): config to define sensor.

        Raises:
            ValueError: there is no available sensor type for the item from config.
        Returns:
            (Sensor): sensor created from config.
        """
        name: str = cfg.name
        sensor_type: str = cfg.type
        params: ParameterConfig = cfg.config
        sensor: Sensor

        match sensor_type:
            case Imu.__name__:
                sensor = Imu(name, params)
            case Fog.__name__:
                sensor = Fog(name, params)
            case Altimeter.__name__:
                sensor = Altimeter(name, params)
            case Lidar2D.__name__:
                sensor = Lidar2D(name, params)
            case Lidar3D.__name__:
                sensor = Lidar3D(name, params)
            case Encoder.__name__:
                sensor = Encoder(name, params)
            case StereoCamera.__name__:
                sensor = StereoCamera(name, params)
            case Gps.__name__:
                sensor = Gps(name, params)
            case VrsGps.__name__:
                sensor = VrsGps(name, params)
            case _:
                msg = f"unsupported sensor type: {sensor_type}"
                logger.error(msg)
                raise ValueError(msg)

        return sensor
