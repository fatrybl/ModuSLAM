import logging
from collections.abc import Sequence

import cv2
import numpy as np

from moduslam.logger.logging_config import frontend_manager
from moduslam.types.numpy import VectorN
from moduslam.utils.auxiliary_dataclasses import VisualFeature

logger = logging.getLogger(frontend_manager)


class FeatureMatcher:
    def __init__(self):
        self._bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self._min_required_matches: int = 4
        self._ransac_reproj_threshold: float = 0.5
        self._num_matches: int | None = None

    def find_matches(self, descriptors_1: VectorN, descriptors_2: VectorN) -> Sequence[cv2.DMatch]:
        """Find matches between two sets of descriptors using a brute-force matcher.

        Args:
            descriptors_1: descriptors of the first set.

            descriptors_2: descriptors of the second set.

        Returns:
            matches.
        """
        matches = self._bf.match(descriptors_1, descriptors_2)
        matches_sorted = sorted(matches, key=lambda x: x.distance)
        if self._num_matches:
            return matches_sorted[: self._num_matches]
        else:
            return matches_sorted

    def filter_with_ransac(
        self,
        keypoints_1: list[cv2.KeyPoint],
        keypoints_2: list[cv2.KeyPoint],
        matches: Sequence[cv2.DMatch],
    ) -> list[cv2.DMatch]:
        """Validate and filter matches with RANSAC.

        Args:
            keypoints_1: keypoints of the first set.

            keypoints_2: keypoints of the second set.

            matches: matches between the sets.

        Returns:
            filtered matches.
        """
        if len(matches) < self._min_required_matches:
            msg = f"Number of matches is less than the required minimum of {self._min_required_matches}."
            logger.error(msg)
            return []

        src_pts = np.array([keypoints_1[m.queryIdx].pt for m in matches]).reshape(-1, 2)
        dst_pts = np.array([keypoints_2[m.trainIdx].pt for m in matches]).reshape(-1, 2)

        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, self._ransac_reproj_threshold)

        matches = [m for i, m in enumerate(matches) if mask[i]]
        return matches

    @staticmethod
    def get_unique_features(
        keypoints: list[cv2.KeyPoint], matches: Sequence[cv2.DMatch]
    ) -> list[cv2.KeyPoint]:
        """Gets unmatched features.

        Args:
            keypoints: keypoints.

            matches: keypoint matches.

        Returns:
            unmatched features.
        """
        matched_indices = {match.queryIdx for match in matches}
        unique_keypoints = [kp for i, kp in enumerate(keypoints) if i not in matched_indices]
        return unique_keypoints

    @staticmethod
    def sort_features(
        new_features: list[VisualFeature], matches: list[cv2.DMatch]
    ) -> tuple[list[VisualFeature], list[int], list[VisualFeature]]:
        """Sorts new visual features into matched and unmatched categories based on
        matches.

        Args:
            new_features: List of new visual features of type VisualFeature.

            matches: List of cv2.DMatch objects representing the matches.

        Returns:
            A tuple containing:
                list of matched new visual features.
                list of indices corresponding to the matched features in the existing list of features.
                list of unmatched new visual features.
        """

        matched_features = []
        matched_indices = []
        matched_indices_set = set()

        for match in matches:
            new_feature_idx = match.queryIdx
            existing_feature_idx = match.trainIdx

            matched_features.append(new_features[new_feature_idx])
            matched_indices.append(existing_feature_idx)
            matched_indices_set.add(new_feature_idx)

        unmatched_features = [f for i, f in enumerate(new_features) if i not in matched_indices_set]

        return matched_features, matched_indices, unmatched_features
