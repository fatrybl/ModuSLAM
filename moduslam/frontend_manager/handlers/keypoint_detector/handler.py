"""Detects ORB keypoints and creates a measurement with visual features. The same
measurement noise covariance is used for every keypoint.

TODO: add/remove both stereo images.
"""

import logging
from collections.abc import Sequence

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.handlers.ABC_handler import Handler
from moduslam.frontend_manager.handlers.keypoint_detector.detector import (
    KeypointDetector,
)
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.logger.logging_config import frontend_manager
from moduslam.setup_manager.sensors_factory.sensors import StereoCamera
from moduslam.system_configs.frontend_manager.handlers.visual_odometry import (
    FeatureDetectorConfig,
)
from moduslam.utils.auxiliary_dataclasses import TimeRange, VisualFeature
from moduslam.utils.auxiliary_methods import create_empty_element

logger = logging.getLogger(frontend_manager)


class FeatureDetector(Handler):

    def __init__(self, config: FeatureDetectorConfig):
        """
        Args:
            config: configuration for the feature detector.
        """
        super().__init__(config)
        self._noise_covariance = config.noise_variance
        self._detector = KeypointDetector()

    def process(self, element: Element) -> Measurement | None:
        """Processes the element and returns the measurement with odometry if one has
        been created.

        Args:
            element: element of data batch with stereo images.

        Returns:
            measurement or None.
        """

        sensor = element.measurement.sensor
        image = element.measurement.values[0]

        if not isinstance(sensor, StereoCamera):
            msg = f"Expected sensor to be of type {StereoCamera.__name__}, got {type(element.measurement.sensor)}"
            logger.error(msg)
            raise TypeError(msg)

        features = self._detector.get_visual_features(image, sensor.calibrations)
        empty_element = self._create_empty_element(element)
        measurement = self._create_measurement(empty_element, features, self._noise_covariance)
        return measurement

    def _create_empty_element(self, element: Element) -> Element:
        """Creates an empty element with the same timestamp, location and sensor as the
        given element.

        Args:
            element: element with data.

        Returns:
            empty element.
        """
        return create_empty_element(element)

    def _create_measurement(
        self,
        element: Element,
        features: Sequence[VisualFeature],
        noise_covariance: tuple[float, float],
    ) -> Measurement:
        """Creates a measurement with ORB features.

        Args:
            element: first element.
            features: visual features.
            noise_covariance: noise covariance.

        Returns:
            measurement.
        """
        t_range = TimeRange(element.timestamp, element.timestamp)
        m = Measurement(
            time_range=t_range,
            elements=(element,),
            values=features,
            handler=self,
            noise_covariance=noise_covariance,
        )
        return m
