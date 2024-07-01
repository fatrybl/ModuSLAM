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
from dataclasses import dataclass

import numpy as np

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.handlers.ABC_handler import Handler
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.logger.logging_config import frontend_manager
from moduslam.setup_manager.sensors_factory.sensors import Imu
from moduslam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_methods import create_empty_element
from moduslam.utils.numpy_types import Vector3

logger = logging.getLogger(frontend_manager)


@dataclass
class ImuData:
    angular_velocity: Vector3
    acceleration: Vector3


class ImuDataPreprocessor(Handler):
    """IMU data handler."""

    def __init__(self, config: HandlerConfig):
        super().__init__(config)

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

        acceleration = np.array(element.measurement.values[10:13], dtype=np.float64)
        angular_velocity = np.array(element.measurement.values[7:10], dtype=np.float64)

        imu_data = ImuData(angular_velocity, acceleration)

        t_range = TimeRange(element.timestamp, element.timestamp)

        acc_cov = tuple(element.measurement.sensor.accelerometer_noise_covariance.flatten())
        gyro_cov = tuple(element.measurement.sensor.gyroscope_noise_covariance.flatten())
        acc_bias_cov = tuple(
            element.measurement.sensor.accelerometer_bias_noise_covariance.flatten()
        )
        gyro_bias_cov = tuple(element.measurement.sensor.gyroscope_bias_noise_covariance.flatten())

        empty_element = self._create_empty_element(element)

        m = Measurement(
            time_range=t_range,
            values=imu_data,
            handler=self,
            elements=(empty_element,),
            noise_covariance=(*acc_cov, *gyro_cov, *acc_bias_cov, *gyro_bias_cov),
        )

        return m

    def _create_empty_element(self, element: Element) -> Element:
        """
        Creates an empty element with the same timestamp, location and sensor as the input element.
        Args:
            element: element of a data batch with raw data.

        Returns:
            empty element without data.
        """
        empty_element = create_empty_element(element)
        return empty_element
