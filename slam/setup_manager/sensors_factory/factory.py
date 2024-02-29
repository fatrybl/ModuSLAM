import logging

from slam.setup_manager.sensors_factory.sensors import (
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
from slam.system_configs.system.setup_manager.sensors_factory import (
    SensorConfig,
    SensorFactoryConfig,
)
from slam.utils.exceptions import SensorNotFound

logger = logging.getLogger(__name__)


class SensorFactory:
    """Factory class for sensors management.

    Class Attributes:
        parameters: sensors to be used in experiments for a particluar dataset.
        used_sensors: sensors to be used in the experiment for a particluar dataset. Must be a subset of parameters.

    Raises:
        SensorNotFound: there is no sensor with the requested sensor name among all sensors.
        NotSubset: some of used sensor are not defined in all sensors set.
        ValueError: there is no available sensor type for the item from config.
    """

    _sensors: set[Sensor] = set()
    _sensors_table: dict[str, Sensor] = {}

    @classmethod
    def all_sensors(cls) -> set[Sensor]:
        """All sensors which have been used in experiment.

        Returns:
            (set[Sensor]): used sensors which have been used in experiment.
        """
        return cls._sensors

    @classmethod
    def get_sensor(cls, name: str) -> Sensor:
        """Maps sensor name to Sensor (if exists) and returns the corresponding sensor.

        Args:
            name (str): sensor name

        Raises:
            SensorNotFound: there is no sensor with the requested sensor name among all sensors.

        Returns:
            Type[Sensor]: sensor if it exists among all sensors.
        """
        try:
            return cls._sensors_table[name]
        except KeyError:
            msg = f"No sensor with the name {name!r} in {cls._sensors}."
            logger.critical(msg)
            raise SensorNotFound(msg)

    @classmethod
    def init_sensors(cls, cfg: SensorFactoryConfig) -> None:
        """Initializes sensors from config.

        Args:
            cfg (SensorFactoryConfig): config to define sensors.
        Raises:
            AssertionError: empty sensors` config.
        """
        assert len(cfg.sensors) > 0, "No sensors defined in the config."

        cls._sensors.clear()
        cls._sensors_table.clear()

        sensors_dict: dict[str, SensorConfig] = cfg.sensors

        for config in sensors_dict.values():
            sensor = cls.sensor_from_config(config)
            cls._sensors.add(sensor)
            cls._sensors_table[sensor.name] = sensor

    @staticmethod
    def sensor_from_config(cfg: SensorConfig) -> Sensor:
        """Creates sensor from config item.

        Args:
            cfg (SensorConfig): config to define sensor.

        Raises:
            ValueError: there is no available sensor type for the item from config.
        Returns:
            (Sensor): sensor created from config.
        """
        name: str = cfg.name
        sensor_type: str = cfg.type_name
        sensor: Sensor

        match sensor_type:
            case Imu.__name__:
                sensor = Imu(name, cfg)
            case Fog.__name__:
                sensor = Fog(name, cfg)
            case Altimeter.__name__:
                sensor = Altimeter(name, cfg)
            case Lidar2D.__name__:
                sensor = Lidar2D(name, cfg)
            case Lidar3D.__name__:
                sensor = Lidar3D(name, cfg)
            case Encoder.__name__:
                sensor = Encoder(name, cfg)
            case StereoCamera.__name__:
                sensor = StereoCamera(name, cfg)
            case Gps.__name__:
                sensor = Gps(name, cfg)
            case VrsGps.__name__:
                sensor = VrsGps(name, cfg)
            case _:
                msg = f"unsupported sensor type: {sensor_type}"
                logger.error(msg)
                raise ValueError(msg)

        return sensor
