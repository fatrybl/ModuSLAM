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

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.handlers.imu_data_preprocessor.line_parsers import (
    get_tum_vie_imu_data,
)
from moduslam.frontend_manager.handlers.interface import Handler
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.logger.logging_config import frontend_manager
from moduslam.setup_manager.sensors_factory.sensors import Imu
from moduslam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_methods import create_empty_element

logger = logging.getLogger(frontend_manager)


class ImuDataPreprocessor(Handler):
    """IMU data handler."""

    def __init__(self, config: HandlerConfig):
        self._name = config.name

    @property
    def name(self) -> str:
        """Unique handler name."""
        return self._name

    def process(self, element: Element) -> Measurement | None:
        """Processes the element with raw IMU data and returns the measurement.

        Args:
            element: an element with raw IMU data.

        Returns:
            new measurement.
        """
        if not isinstance(element.measurement.sensor, Imu):
            msg = f"Expected sensor of type {Imu}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        imu_data = get_tum_vie_imu_data(element.measurement.values)

        t_range = TimeRange(element.timestamp, element.timestamp)

        acc_cov = element.measurement.sensor.accelerometer_noise_covariance
        gyro_cov = element.measurement.sensor.gyroscope_noise_covariance
        acc_bias_cov = element.measurement.sensor.accelerometer_bias_noise_covariance
        gyro_bias_cov = element.measurement.sensor.gyroscope_bias_noise_covariance

        empty_element = self.create_empty_element(element)

        m = Measurement(
            time_range=t_range,
            value=imu_data,
            handler=self,
            elements=(empty_element,),
            noise_covariance=(acc_cov, gyro_cov, acc_bias_cov, gyro_bias_cov),
        )

        return m

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
