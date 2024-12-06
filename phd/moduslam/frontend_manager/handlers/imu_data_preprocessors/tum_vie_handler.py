"""
    IMU data format: [
            timestamp,
            quaternion x, quaternion y, quaternion z, quaternion w,
            Euler x, Euler y, Euler z,
            Gyro x, Gyro y, Gyro z,
            Acceleration x, Acceleration y, Acceleration z,
            MagnetField x, MagnetField y, MagnetField z
            ]

    timestamp is not present in element`s raw data.

    Transform IMU data to the base frame according to the transformation matrix tf_base_sensor:
    https://github.com/TixiaoShan/LIO-SAM/issues/204#issuecomment-788827042
"""

import logging

from phd.logger.logging_config import frontend_manager
from phd.measurements.processed import Imu as ImuMeasurement
from phd.moduslam.custom_types.aliases import Matrix4x4
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.frontend_manager.handlers.handler_protocol import Handler
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.config import (
    ImuHandlerConfig,
)
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.objects import (
    ImuCovariance,
    ImuData,
)
from phd.moduslam.setup_manager.sensors_factory.sensors import Imu as ImuSensor
from phd.moduslam.utils.auxiliary_methods import create_empty_element, str_to_float

logger = logging.getLogger(frontend_manager)


class TumVieImuDataPreprocessor(Handler):
    """Tum Vie IMU data preprocessor."""

    def __init__(self, config: ImuHandlerConfig):
        self._sensor_name = config.sensor_name

    @property
    def sensor_name(self) -> str:
        """Unique handler name."""
        return self._sensor_name

    @property
    def sensor_type(self) -> type[ImuSensor]:
        """IMU sensor type."""
        return ImuSensor

    def process(self, element: Element) -> ImuMeasurement | None:
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

        imu_data = self._parse_line(element.measurement.values)

        tf = self._create_tf(sensor)

        covariance = self._create_covariance(sensor)

        empty_element = self.create_empty_element(element)

        return ImuMeasurement(empty_element, imu_data, covariance, tf)

    @staticmethod
    def create_empty_element(element: Element) -> Element:
        """
        Creates an empty element with the same timestamp, location and sensor as the input element.
        Args:
            element: element of a data batch with raw data.

        Returns:
            empty element without data.
        """
        return create_empty_element(element)

    @staticmethod
    def _parse_line(values: tuple[str, ...]) -> ImuData:
        """Extracts IMU raw data from an element created with the TUM VIE dataset.

        Args:
            values: an imu data.

        Returns:
            IMU data.
        """
        wx = str_to_float(values[0])
        wy = str_to_float(values[1])
        wz = str_to_float(values[2])
        ax = str_to_float(values[3])
        ay = str_to_float(values[4])
        az = str_to_float(values[5])
        return ImuData((wx, wy, wz), (ax, ay, az))

    @staticmethod
    def _create_tf(sensor: ImuSensor) -> Matrix4x4:
        tf = sensor.tf_base_sensor
        pose = (
            (tf[0][0], tf[0][1], tf[0][2], tf[0][3]),
            (tf[1][0], tf[1][1], tf[1][2], tf[1][3]),
            (tf[2][0], tf[2][1], tf[2][2], tf[2][3]),
            (0.0, 0.0, 0.0, 1.0),
        )
        return pose

    @staticmethod
    def _create_covariance(sensor: ImuSensor) -> ImuCovariance:
        """Creates IMU covariances using the given sensor.

        Args:
            sensor: an IMU sensor.

        Returns: IMU covariance.
        """
        a = sensor.accelerometer_noise_covariance
        g = sensor.gyroscope_noise_covariance
        a_bias = sensor.accelerometer_bias_noise_covariance
        g_bias = sensor.gyroscope_bias_noise_covariance
        integ = sensor.integration_noise_covariance

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

        integr_cov = (
            (integ[0][0], integ[0][1], integ[0][2]),
            (integ[1][0], integ[1][1], integ[1][2]),
            (integ[2][0], integ[2][1], integ[2][2]),
        )

        covariances = ImuCovariance(accel_cov, gyro_cov, accel_bias_cov, gyro_bias_cov, integr_cov)
        return covariances
