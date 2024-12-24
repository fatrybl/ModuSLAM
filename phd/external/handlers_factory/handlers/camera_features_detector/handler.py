"""Detects ORB keypoints and creates a measurement with visual features.

The same measurement noise covariance is used for every keypoint.
"""

import logging
from collections.abc import Sequence

from moduslam.logger.logging_config import frontend_manager
from phd.external.handlers_factory.handlers.camera_features_detector.config import (
    FeatureDetectorConfig,
)
from phd.external.handlers_factory.handlers.camera_features_detector.detector import (
    KeypointDetector,
)
from phd.external.handlers_factory.handlers.handler_protocol import Handler
from phd.measurement_storage.measurements.base import WithRawElements
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.utils import create_empty_element
from phd.moduslam.sensors_factory.sensors import StereoCamera
from phd.utils.auxiliary_dataclasses import VisualFeature

logger = logging.getLogger(frontend_manager)


class FeatureDetector(Handler):

    def __init__(self, config: FeatureDetectorConfig):
        """
        Args:
            config: configuration for the feature detector.
        """
        self._name = config.sensor_name
        self._noise_covariance = config.noise_variance
        self._detector = KeypointDetector(num_features=1000)

    @property
    def sensor_name(self) -> str:
        """Unique handler name."""
        return self._name

    def process(self, element: Element) -> WithRawElements | None:
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
            msg = f"Expected sensor to be of type {StereoCamera.__name__}, got {type(sensor)!r}."
            logger.error(msg)
            raise TypeError(msg)

        features = self._detector.get_visual_features(image)
        empty_element = create_empty_element(element)
        measurement = self._create_measurement(empty_element, features, self._noise_covariance)
        return measurement

    def _create_measurement(
        self,
        element: Element,
        features: Sequence[VisualFeature],
        noise_covariance: tuple[float, float],
    ) -> WithRawElements:
        """Creates a measurement with ORB features.

        Args:
            element: first element.

            features: visual features.

            noise_covariance: noise covariance.

        Returns:
            measurement.
        """
        # t_range = TimeRange(element.timestamp, element.timestamp)
        # m = Measurement(
        #     time_range=t_range,
        #     elements=(element,),
        #     value=features,
        #     handler=self,
        #     noise_covariance=noise_covariance,
        # )
        # return m
        raise NotImplementedError
