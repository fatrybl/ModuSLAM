import logging
from collections import deque
from collections.abc import Sequence
from typing import Iterable, TypeAlias

import cv2
import numpy as np

from moduslam.frontend_manager.edge_factories.smart_visual_features.feature_matcher import (
    FeatureMatcher,
)
from moduslam.frontend_manager.graph.custom_edges import SmartVisualFeature
from moduslam.logger.logging_config import frontend_manager
from moduslam.utils.auxiliary_dataclasses import VisualFeature

logger = logging.getLogger(frontend_manager)

FeatureWithEdge: TypeAlias = tuple[VisualFeature, SmartVisualFeature]


class VisualFeatureStorage:
    def __init__(self):
        self._items: deque[FeatureWithEdge] = deque()
        self._matcher = FeatureMatcher()

    @property
    def visual_features(self) -> list[VisualFeature]:
        """All visual features in the storage."""
        return [tup[0] for tup in self._items]

    @property
    def items(self) -> deque[FeatureWithEdge]:
        """All features and edges."""
        return self._items

    @staticmethod
    def get_unmatched_features(
        features: Sequence[VisualFeature], matches: Iterable[cv2.DMatch]
    ) -> list[VisualFeature]:
        """Gets unmatched visual features.

        Args:
            features: visual features.

            matches: visual feature matches.

        Returns:
            list of unmatched features.
        """
        if not matches:
            return list(features)

        unmatched_features = []
        matched_indices = {match.queryIdx for match in matches}

        for i, feature in enumerate(features):
            if i not in matched_indices:
                unmatched_features.append(feature)

        return unmatched_features

    def get_matches(self, new_features: list[VisualFeature]) -> list[cv2.DMatch]:
        """Match ORB keypoints and descriptors between two images and filters matches
        with RANSAC.

        Args:
            new_features: visual features.

        Returns:
            filtered matches and unmatched features.
        """
        if not self._items:
            return []

        existing_features = self.visual_features

        keypoints_1 = [f.key_point for f in new_features]
        descriptors_1 = np.array([f.descriptor for f in new_features])

        keypoints_2 = [f.key_point for f in existing_features]
        descriptors_2 = np.array([f.descriptor for f in existing_features])

        matches = self._matcher.find_matches(descriptors_1, descriptors_2)
        filtered_matches = self._matcher.filter_with_ransac(keypoints_1, keypoints_2, matches)

        return filtered_matches

    def get_feature_with_edge(self, feature_index: int) -> FeatureWithEdge:
        """Gets the visual feature and the edge.

        Args:
            feature_index: index of the visual feature.

        Returns:
            visual feature and corresponding edge.
        """
        tup = self._items[feature_index]
        return tup

    def add(self, feature: VisualFeature, edge: SmartVisualFeature) -> None:
        """Adds new item.

        Args:
            feature: visual feature.

            edge: edge with smart factor.
        """
        self._items.append((feature, edge))

    def remove_old_features(self) -> None:
        """Removes all features with the timestamp of the 1-st feature in the
        storage."""

        num_features: int = 0
        feature, edge = self._items[0]
        vertex = edge.central_vertex
        timestamp = vertex.timestamp

        for index, tup in enumerate(self._items):
            _, edge = tup
            if edge.central_vertex.timestamp == timestamp:
                num_features += 1
                break

        for _ in range(num_features):
            self._items.popleft()
