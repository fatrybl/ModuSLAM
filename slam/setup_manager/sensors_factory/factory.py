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
from slam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(__name__)


class SensorsFactory:
    """Factory class for sensors.

    Class Attributes:
        parameters: sensors to be used in experiments for a particular dataset.
        used_sensors: sensors to be used in the experiment for a particular dataset. Must be a subset of parameters.

    Raises:
        ItemNotFoundError: no sensor with the requested sensor name in all sensors.
        ValueError: non-existing sensor`s type for the item from config.
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
            ItemNotFoundError: there is no sensor with the requested sensor name among all sensors.

        Returns:
            Type[Sensor]: sensor if it exists among all sensors.
        """
        try:
            return cls._sensors_table[name]
        except KeyError:
            msg = f"No sensor with the name {name!r} in {cls._sensors}."
            raise ItemNotFoundError(msg)

    @classmethod
    def init_sensors(cls, cfg: SensorFactoryConfig) -> None:
        """Initializes sensors from config.

        Args:
            cfg (SensorFactoryConfig): config to define sensors.
        Raises:
            ValueError: empty sensors` config.
        """
        if not cfg.sensors:
            msg = "Empty sensors config."
            logger.error(msg)
            raise ValueError(msg)

        cls._sensors.clear()
        cls._sensors_table.clear()

        for config in cfg.sensors.values():
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

        sensor_type: str = cfg.type_name
        sensor: Sensor

        match sensor_type:

            case Sensor.__name__:
                sensor = Sensor(cfg)
            case Imu.__name__:
                sensor = Imu(cfg)
            case Fog.__name__:
                sensor = Fog(cfg)
            case Altimeter.__name__:
                sensor = Altimeter(cfg)
            case Lidar2D.__name__:
                sensor = Lidar2D(cfg)
            case Lidar3D.__name__:
                sensor = Lidar3D(cfg)
            case Encoder.__name__:
                sensor = Encoder(cfg)
            case StereoCamera.__name__:
                sensor = StereoCamera(cfg)
            case Gps.__name__:
                sensor = Gps(cfg)
            case VrsGps.__name__:
                sensor = VrsGps(cfg)
            case _:
                msg = f"unsupported sensor type: {sensor_type}"
                logger.error(msg)
                raise ValueError(msg)

        return sensor
