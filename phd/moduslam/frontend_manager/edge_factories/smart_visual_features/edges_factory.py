from collections.abc import Iterable, Sequence

import cv2
import numpy as np

from moduslam.frontend_manager.edge_factories.smart_visual_features.smart_factor_factory import (
    SmartFactorFactory,
)
from moduslam.frontend_manager.edge_factories.smart_visual_features.storage import (
    FeatureWithEdge,
)
from moduslam.frontend_manager.graph.custom_edges import SmartVisualFeature
from moduslam.frontend_manager.graph.custom_vertices import CameraPose, Feature3D
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.frontend_manager.noise_models import pixel_diagonal_noise_model
from moduslam.setup_manager.sensors_factory.sensors import StereoCamera
from moduslam.utils.auxiliary_dataclasses import VisualFeature


class EdgesFactory:

    def __init__(self):
        self._smart_factor_factory = SmartFactorFactory()

    @staticmethod
    def update_edge(
        edge: SmartVisualFeature,
        vertex: CameraPose,
        keypoint: cv2.KeyPoint,
        measurement: Measurement,
    ):
        """Updates the edge with the new measured feature.

        Args:
            edge: edge to update.

            vertex: new vertex with the visual feature.

            keypoint: new keypoint.

            measurement: measurement with visual features.

        Returns:
            updated edge.
        """
        pixels = np.array(keypoint.pt)

        edge.radial_vertices.append(vertex)
        edge.measurements.append(measurement)
        edge.factor.add(pixels, vertex.backend_index)
        return edge

    def create_edges(
        self,
        measurement: Measurement,
        base_vertex: CameraPose,
        sensor: StereoCamera,
        features: Sequence[VisualFeature],
    ) -> list[SmartVisualFeature]:
        """Creates edges for the visual features.

        Args:
            measurement: measurement with visual feature.

            base_vertex: vertex with camera pose.

            sensor: sensor with the camera calibration.

            features: visual features.

        Returns:
            new edge.
        """
        edges: list[SmartVisualFeature] = []
        tf = np.array(sensor.tf_base_sensor)
        camera_matrix = np.array(sensor.calibrations.camera_matrix_left)
        variance = (measurement.noise_covariance[0], measurement.noise_covariance[1])
        noise = pixel_diagonal_noise_model(variance)

        for feature in features:
            m = self._create_measurement(measurement, feature)
            vertex = Feature3D(base_vertex.index, base_vertex.timestamp)
            factor = self._smart_factor_factory.create(tf, camera_matrix, noise)
            edge = SmartVisualFeature(vertex, [], [], factor, noise)
            edge = EdgesFactory.update_edge(edge, base_vertex, feature.key_point, m)
            edges.append(edge)

        return edges

    @staticmethod
    def _create_measurement(measurement: Measurement, feature: VisualFeature):
        """Creates a measurement with the visual feature.

        Args:
            measurement: measurement with the camera pose.

            feature: visual feature.

        Returns:
            new measurement.
        """
        return Measurement(
            time_range=measurement.time_range,
            value=feature,
            noise_covariance=measurement.noise_covariance,
            elements=measurement.elements,
            handler=measurement.handler,
        )

    @staticmethod
    def modify_edges(
        features_with_edges: Sequence[FeatureWithEdge],
        matches: Iterable[cv2.DMatch],
        features: list[VisualFeature],
        base_vertex: CameraPose,
        measurement: Measurement,
    ) -> list[SmartVisualFeature]:
        """Modifies the edges.

        Returns:
            modified edges.
        """
        edges = []
        for match in matches:
            new_feature = features[match.queryIdx]
            vertex, edge = features_with_edges[match.trainIdx]
            edge = EdgesFactory.update_edge(edge, base_vertex, new_feature.key_point, measurement)
            edges.append(edge)

        return edges
