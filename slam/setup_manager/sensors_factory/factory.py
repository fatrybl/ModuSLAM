import logging
from typing import cast

from slam.logger.logging_config import setup_manager
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
from slam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from slam.system_configs.setup_manager.sensors import Lidar3DConfig, SensorConfig
from slam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(setup_manager)


class SensorsFactory:
    """Creates and stores sensors."""

    _sensors: set[Sensor] = set()
    _sensors_table: dict[str, Sensor] = {}

    @classmethod
    def get_sensors(cls) -> set[Sensor]:
        """Gets all sensors."""
        return cls._sensors

    @classmethod
    def get_sensor(cls, name: str) -> Sensor:
        """Gets sensor with the given name.

        Args:
            name: name of a sensor.

        Returns:
            sensor.

        Raises:
            ItemNotFoundError: if no sensor with the given name.
        """
        try:
            return cls._sensors_table[name]
        except KeyError:
            msg = f"No sensor with the name {name!r} in {cls._sensors}."
            raise ItemNotFoundError(msg)

    @classmethod
    def init_sensors(cls, config: SensorFactoryConfig) -> None:
        """Initializes sensors for the given configuration.

        Args:
            config: sensors` configuration.
        """
        cls._sensors.clear()
        cls._sensors_table.clear()

        for cfg in config.sensors.values():
            sensor = cls.sensor_from_config(cfg)
            cls._sensors.add(sensor)
            cls._sensors_table[sensor.name] = sensor

    @staticmethod
    def sensor_from_config(config: SensorConfig) -> Sensor:
        """Creates sensor with the given configuration.

        Args:
            config: sensor configuration.

        Returns:
            sensor.

        Raises:
            ValueError: if sensor type is not supported.
        """

        sensor_type: str = config.type_name

        match sensor_type:

            case Sensor.__name__:
                sensor = Sensor(config)
            case Imu.__name__:
                sensor = Imu(config)
            case Fog.__name__:
                sensor = Fog(config)
            case Altimeter.__name__:
                sensor = Altimeter(config)
            case Lidar2D.__name__:
                sensor = Lidar2D(config)
            case Lidar3D.__name__:
                config = cast(Lidar3DConfig, config)
                sensor = Lidar3D(config)
            case Encoder.__name__:
                sensor = Encoder(config)
            case StereoCamera.__name__:
                sensor = StereoCamera(config)
            case Gps.__name__:
                sensor = Gps(config)
            case VrsGps.__name__:
                sensor = VrsGps(config)
            case _:
                msg = f"Unsupported sensor type: {sensor_type}"
                logger.critical(msg)
                raise ValueError(msg)

        return sensor
