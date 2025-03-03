import logging
from typing import cast

from src.logger.logging_config import setup_manager
from src.moduslam.sensors_factory.configs import (
    ImuConfig,
    Lidar3DConfig,
    SensorConfig,
    StereoCameraConfig,
    VrsGpsConfig,
)
from src.moduslam.sensors_factory.sensors import (
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
from src.utils.exceptions import ItemNotExistsError

logger = logging.getLogger(setup_manager)


class SensorsFactory:
    """Creates and stores sensors."""

    _sensors: set[Sensor] = set()
    _sensors_table: dict[str, Sensor] = {}

    @classmethod
    def get_all_sensors(cls) -> set[Sensor]:
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
            ItemNotExistsError: no sensor exists with the given name.
        """
        try:
            return cls._sensors_table[name]
        except KeyError:
            msg = f"No sensor with the name {name!r} in {cls._sensors}."
            raise ItemNotExistsError(msg)

    @classmethod
    def init_sensors(cls, sensors: dict[str, SensorConfig]) -> None:
        """Initializes sensors for the given configuration.

        Args:
            sensors: "sensor name <-> sensor config" table.

        Raises:
            ValueError: if sensor`s name does not match the name in the config.
        """
        cls._sensors.clear()
        cls._sensors_table.clear()

        for name, config in sensors.items():

            if name != config.name:
                msg = "Sensor`s name does not match the name in the config."
                logger.critical(msg)
                raise ValueError(msg)

            sensor = cls.sensor_from_config(config)
            cls._sensors.add(sensor)
            cls._sensors_table[sensor.name] = sensor

    @classmethod
    def clear(cls) -> None:
        """Deletes all sensors from the factory."""
        cls._sensors.clear()
        cls._sensors_table.clear()

    @staticmethod
    def sensor_from_config(config: SensorConfig) -> Sensor:
        """Creates sensor with the given configuration.

        Args:
            config: sensor configuration.

        Returns:
            sensor.

        Raises:
            TypeError: if sensor`s type is not supported.
        """

        sensor_type: str = config.type_name

        match sensor_type:

            case Sensor.__name__:
                sensor = Sensor(config.name)
            case Imu.__name__:
                config = cast(ImuConfig, config)
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
                config = cast(StereoCameraConfig, config)
                sensor = StereoCamera(config)
            case Gps.__name__:
                sensor = Gps(config)
            case VrsGps.__name__:
                config = cast(VrsGpsConfig, config)
                sensor = VrsGps(config)
            case _:
                msg = f"Unsupported sensor type: {sensor_type}"
                logger.critical(msg)
                raise TypeError(msg)

        return sensor
