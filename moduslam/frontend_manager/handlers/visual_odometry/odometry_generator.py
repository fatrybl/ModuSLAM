"""Visual Odometry Handler.

Does not utilize both images of stereo pair. Uses only left image for odometry
computation.
"""

import logging

import numpy as np
from PIL.Image import Image

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.handlers.ABC_handler import Handler
from moduslam.frontend_manager.handlers.visual_odometry.camera_features import (
    compute_transformation,
    get_orb_features,
    get_points_and_pixels,
    match_keypoints,
)
from moduslam.frontend_manager.handlers.visual_odometry.depth_estimator import (
    DepthEstimator,
)
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.logger.logging_config import frontend_manager
from moduslam.setup_manager.sensors_factory.sensors import StereoCamera
from moduslam.system_configs.frontend_manager.handlers.visual_odometry import (
    VisualOdometryConfig,
)
from moduslam.system_configs.setup_manager.sensors import StereoCameraConfig
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_methods import create_empty_element
from moduslam.utils.numpy_types import Matrix4x4

logger = logging.getLogger(frontend_manager)


class VisualOdometry(Handler):

    def __init__(self, config: VisualOdometryConfig):
        super().__init__(config)
        self._skip_n_frames: int = config.skip_n_frames
        self._noise_covariance = config.noise_variance
        self._depth_model = DepthEstimator()
        self._queue: list[Element] = []
        self._queue_size: int = 2
        self._counter: int = 0

    def process(self, element: Element) -> Measurement | None:
        """Processes the element and returns the measurement with odometry if one has
        been created.

        Args:
            element: element of data batch with stereo iamges.

        Returns:
            measurement or None.
        """

        sensor = element.measurement.sensor
        if not isinstance(sensor, StereoCamera):
            msg = f"Expected sensor to be of type {StereoCamera.__name__}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        self._counter += 1
        tf_base_sensor = sensor.tf_base_sensor
        tf_base_sensor_inv = np.linalg.inv(tf_base_sensor)

        if self._counter > self._skip_n_frames:
            self._queue.append(element)
            self._counter = 0

        if len(self._queue) < self._queue_size:
            return None

        else:
            element1 = self._queue.pop(0)
            element2 = self._queue[0]

            img1 = element1.measurement.values[0]
            img2 = element2.measurement.values[0]

            tf_odom = self._compute_odometry(img1, img2, sensor.calibrations)
            tf_base = tf_base_sensor @ tf_odom @ tf_base_sensor_inv

            empty_element1 = self._create_empty_element(element1)
            empty_element2 = self._create_empty_element(element2)

            measurement = self._create_measurement(
                empty_element1, empty_element2, tf_base, self._noise_covariance
            )
            return measurement

    def _compute_odometry(
        self, image1: Image, image2: Image, camera_parameters: StereoCameraConfig
    ) -> Matrix4x4:
        """Computes odometry between two images.

        Args:
            image1: first image.
            image2: second image.
            camera_parameters: camera parameters.

        Returns:
            transformation matrix and noise covariance.
        """

        image1_np, image2_np = np.array(image1), np.array(image2)
        camera_matrix = np.array(camera_parameters.camera_matrix_left)
        distortion_coefficients = np.array(camera_parameters.distortion_coefficients_left)

        keypoints1, descriptors1 = get_orb_features(image1_np)
        keypoints2, descriptors2 = get_orb_features(image2_np)

        common_keypoints = match_keypoints(descriptors1, descriptors2)

        depth_1 = self._depth_model.estimate_depth(image1)
        depth_2 = self._depth_model.estimate_depth(image2)

        points, pixels = get_points_and_pixels(
            depth_1,
            depth_2,
            keypoints1,
            keypoints2,
            common_keypoints,
            camera_matrix,
        )

        tf = compute_transformation(
            points,
            pixels,
            camera_matrix,
            distortion_coefficients,
        )
        return tf

    def _create_empty_element(self, element: Element) -> Element:
        """Creates an empty element with the same timestamp, location and sensor as the
        given element."""
        return create_empty_element(element)

    def _create_measurement(
        self,
        element1: Element,
        element2: Element,
        tf: Matrix4x4,
        noise_covariance: tuple[float, float, float, float, float, float],
    ) -> Measurement:
        """Creates a measurement with odometry.

        Args:
            element1: first element.
            element2: second element.
            tf: transformation matrix.
            noise_covariance: noise covariance.

        Returns:
            measurement.
        """
        t_range = TimeRange(element1.timestamp, element2.timestamp)
        m = Measurement(
            time_range=t_range,
            elements=(element1, element2),
            values=tf,
            handler=self,
            noise_covariance=noise_covariance,
        )
        return m
