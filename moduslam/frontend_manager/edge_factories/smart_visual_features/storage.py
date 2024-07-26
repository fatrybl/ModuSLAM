import logging
from collections import deque
from typing import TypeAlias

import gtsam
import numpy as np

from moduslam.frontend_manager.edge_factories.smart_visual_features.feature_matcher import (
    FeatureMatcher,
)
from moduslam.frontend_manager.graph.custom_vertices import Feature3D
from moduslam.logger.logging_config import frontend_manager
from moduslam.utils.auxiliary_dataclasses import VisualFeature

logger = logging.getLogger(frontend_manager)

VisualFeatureTuple: TypeAlias = tuple[VisualFeature, Feature3D, gtsam.SmartProjectionPose3Factor]


class VisualFeatureStorage:
    def __init__(self):
        self._features: deque[VisualFeatureTuple] = deque()
        self._matcher = FeatureMatcher()

    @property
    def visual_features(self) -> list[VisualFeature]:
        """All visual features in the storage."""
        return [tup[0] for tup in self._features]

    def get_features(
        self, new_features: list[VisualFeature]
    ) -> tuple[list[VisualFeature], list[int], list[VisualFeature]]:
        """Match ORB keypoints and descriptors between two images using RANSAC.

        Args:
            new_features: visual features.

        Returns:
            list of matched features, indices of matched features, and unmatched features.
        """
        if not self._features:
            return [], [], new_features

        existing_features = self.visual_features

        keypoints_1 = [f.key_point for f in new_features]
        descriptors_1 = np.array([f.descriptor for f in new_features]).squeeze()

        keypoints_2 = [f.key_point for f in existing_features]
        descriptors_2 = np.array([f.descriptor for f in existing_features]).squeeze()

        matches = self._matcher.find_matches(descriptors_1, descriptors_2)
        filtered_matches = self._matcher.filter_with_ransac(keypoints_1, keypoints_2, matches)

        matched_features, matched_features_indices, unmatched_features = (
            self._matcher.sort_features(new_features, filtered_matches)
        )

        return matched_features, matched_features_indices, unmatched_features

    def get_vertex_and_factor(
        self, feature_index: int
    ) -> tuple[Feature3D, gtsam.SmartProjectionPose3Factor]:
        """Gets the vertex and the factor of the existing visual feature.

        Args:
            feature_index: index of the visual feature.

        Returns:
            camera feature vertex and GTSAM smart projection factor.
        """
        tup = self._features[feature_index]
        vertex, factor = tup[1], tup[2]
        return vertex, factor

    def add(
        self, feature: VisualFeature, vertex: Feature3D, factor: gtsam.SmartProjectionPose3Factor
    ) -> None:
        """Adds new item.

        Args:
            feature: visual feature.

            vertex: feature vertex.

            factor: GTSAM factor.
        """
        self._features.append((feature, vertex, factor))

    def remove_old_features(self) -> None:
        """Removes all features with the timestamp of the 1-st feature in the
        storage."""

        num_features: int = 0
        _, vertex, _ = self._features[0]
        timestamp = vertex.timestamp

        for index, tup in enumerate(self._features):
            feature, vertex, _ = tup
            if vertex.timestamp == timestamp:
                num_features += 1
            else:
                break

        for _ in range(num_features):
            self._features.popleft()
