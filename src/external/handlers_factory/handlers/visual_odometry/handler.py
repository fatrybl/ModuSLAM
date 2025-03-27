"""Detects ORB keypoints and creates a measurement with visual features.

The same measurement noise covariance is used for every keypoint.
"""

import logging

import numpy as np

from src.custom_types.numpy import Matrix4x4
from src.external.handlers_factory.handlers.handler_protocol import Handler
from src.external.handlers_factory.handlers.visual_odometry.config import (
    VisualOdometryConfig,
)
from src.external.handlers_factory.handlers.visual_odometry.monocular.image_processing import (
    compute_transformation,
)
from src.logger.logging_config import frontend_manager
from src.measurement_storage.measurements.pose_odometry import OdometryWithElements
from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.utils import create_empty_element
from src.moduslam.sensors_factory.sensors import StereoCamera
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_methods import diagonal_matrix3x3, numpy_array4x4_to_tuple4x4

logger = logging.getLogger(frontend_manager)


class VisualOdometry(Handler):
    """Creates a measurement with the transformation between 2 images."""

    _NUM_ELEMENTS = 2

    def __init__(self, config: VisualOdometryConfig):
        """
        Args:
            config: configuration for the feature detector.
        """
        self._skip_n_frames = config.skip_n_frames
        self._name = config.sensor_name
        self._covariance = config.measurement_noise_covariance
        self._elements_queue: list[Element] = []
        self._element_counter: int = 0

    @property
    def sensor_name(self) -> str:
        """Unique handler name."""
        return self._name

    @property
    def sensor_type(self) -> type[StereoCamera]:
        """Lidar 3D sensor type."""
        return StereoCamera

    def process(self, element: Element) -> OdometryWithElements | None:
        """Processes the element and returns the measurement with odometry if one has
        been created.

        Args:
            element: element of data batch with stereo images.

        Returns:
            measurement or None.
        """
        sensor = element.measurement.sensor

        if not isinstance(sensor, StereoCamera):
            msg = f"Expected sensor of type {StereoCamera}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        self._element_counter += 1

        if self._skip_n_frames == 0 or (self._element_counter - 1) % (self._skip_n_frames + 1) == 0:
            self._elements_queue.append(element)

        if len(self._elements_queue) == self._NUM_ELEMENTS:
            tf = self._compute_odometry(sensor, self._elements_queue)
            measurement = self._create_empty_measurement(tf)
            self._elements_queue.pop(0)

            return measurement

        return None

    @staticmethod
    def _compute_odometry(sensor: StereoCamera, elements: list[Element]) -> Matrix4x4:
        """Computes odometry between two images.

        Args:
            sensor: stereo camera sensor.
            elements: elements with stereo images.

        Returns:
            SE(3) transformation.
        """
        tf_base_sensor = np.array(sensor.tf_base_sensor)
        tf_base_sensor_inv = np.linalg.inv(tf_base_sensor)

        el1, el2 = elements[0], elements[1]
        prev_img, cur_img = el1.measurement.values[0], el2.measurement.values[0]

        d_tf = compute_transformation(prev_img, cur_img, sensor.calibrations)
        d_tf_base = tf_base_sensor @ d_tf @ tf_base_sensor_inv

        return d_tf_base

    def _create_empty_measurement(self, tf: Matrix4x4) -> OdometryWithElements:
        """Creates the measurement with the computed transformation matrix.

        Args:
            tf: transformation matrix SE(3).

        Returns:
            odometry with elements.
        """
        el1, el2 = self._elements_queue[0], self._elements_queue[1]

        empty_el1 = create_empty_element(el1)
        empty_el2 = create_empty_element(el2)

        start, stop = el1.timestamp, el2.timestamp
        t_range = TimeRange(start, stop)

        cov = self._covariance
        position_covariance = diagonal_matrix3x3(cov[0:3])
        orientation_covariance = diagonal_matrix3x3(cov[3:])

        pose = numpy_array4x4_to_tuple4x4(tf)

        return OdometryWithElements(
            stop,
            t_range,
            pose,
            position_covariance,
            orientation_covariance,
            elements=[empty_el1, empty_el2],
        )
