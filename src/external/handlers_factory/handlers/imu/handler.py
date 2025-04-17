import logging

from src.external.handlers_factory.handlers.handler_protocol import Handler
from src.external.handlers_factory.handlers.imu.config import (
    ImuHandlerConfig,
)
from src.external.handlers_factory.handlers.imu.parsers import dataset_parser_mapping
from src.logger.logging_config import frontend_manager
from src.measurement_storage.measurements.imu import (
    ImuCovariance,
    ProcessedImu,
)
from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.sensors_factory.sensors import Imu as ImuSensor
from src.utils.exceptions import ConfigurationError

logger = logging.getLogger(frontend_manager)


class ImuHandler(Handler):
    """Tum Vie IMU data preprocessor."""

    def __init__(self, config: ImuHandlerConfig):
        self._sensor_name = config.sensor_name

        try:
            self._parser = dataset_parser_mapping[config.data_reader]
        except KeyError:
            msg = f"Parser not found for {config.data_reader}"
            logger.error(msg)
            raise ConfigurationError(msg)

    @property
    def sensor_name(self) -> str:
        """Unique handler name."""
        return self._sensor_name

    @property
    def sensor_type(self) -> type[ImuSensor]:
        """IMU sensor type."""
        return ImuSensor

    def process(self, element: Element) -> ProcessedImu | None:
        """Processes the element with raw IMU data and returns the measurement.

        Args:
            element: an element with raw IMU data.

        Returns:
            new measurement.

        Raises:
            TypeError: If the sensor of the measurement is not an Imu.
        """
        sensor = element.measurement.sensor

        if not isinstance(sensor, ImuSensor):
            msg = f"Expected sensor of type {ImuSensor}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        imu_data = self._parser(element.measurement.values)

        covariance = self._get_covariance(sensor)

        return ProcessedImu(element.timestamp, imu_data, covariance, sensor.tf_base_sensor)

    @staticmethod
    def _get_covariance(sensor: ImuSensor) -> ImuCovariance:
        """Creates IMU covariances using the given sensor.

        Args:
            sensor: an IMU sensor.

        Returns: IMU covariance.
        """
        a = sensor.accelerometer_noise_covariance
        g = sensor.gyroscope_noise_covariance
        a_bias = sensor.accelerometer_bias_noise_covariance
        g_bias = sensor.gyroscope_bias_noise_covariance
        integration = sensor.integration_noise_covariance

        accel_cov = (
            (a[0][0], a[0][1], a[0][2]),
            (a[1][0], a[1][1], a[1][2]),
            (a[2][0], a[2][1], a[2][2]),
        )
        gyro_cov = (
            (g[0][0], g[0][1], g[0][2]),
            (g[1][0], g[1][1], g[1][2]),
            (g[2][0], g[2][1], g[2][2]),
        )
        accel_bias_cov = (
            (a_bias[0][0], a_bias[0][1], a_bias[0][2]),
            (a_bias[1][0], a_bias[1][1], a_bias[1][2]),
            (a_bias[2][0], a_bias[2][1], a_bias[2][2]),
        )
        gyro_bias_cov = (
            (g_bias[0][0], g_bias[0][1], g_bias[0][2]),
            (g_bias[1][0], g_bias[1][1], g_bias[1][2]),
            (g_bias[2][0], g_bias[2][1], g_bias[2][2]),
        )

        integration_cov = (
            (integration[0][0], integration[0][1], integration[0][2]),
            (integration[1][0], integration[1][1], integration[1][2]),
            (integration[2][0], integration[2][1], integration[2][2]),
        )

        covariances = ImuCovariance(
            accel_cov, gyro_cov, accel_bias_cov, gyro_bias_cov, integration_cov
        )
        return covariances
