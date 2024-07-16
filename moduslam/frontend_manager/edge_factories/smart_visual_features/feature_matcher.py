from collections.abc import Sequence

import cv2
import numpy as np

from moduslam.utils.auxiliary_dataclasses import VisualFeature
from moduslam.utils.numpy_types import VectorN


class FeatureMatcher:
    def __init__(self):
        self._bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def find_matches(self, descriptors_1: VectorN, descriptors_2: VectorN) -> Sequence[cv2.DMatch]:
        """Find matches between two sets of descriptors using a brute-force matcher.

        Args:
            descriptors_1: descriptors of the first set.

            descriptors_2: descriptors of the second set.

        Returns:
            matches.
        """
        matches = self._bf.match(descriptors_1, descriptors_2)
        return matches

    @staticmethod
    def filter_with_ransac(
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
        if len(matches) < 4:
            return []

        src_pts = np.array([keypoints_1[m.queryIdx].pt for m in matches]).reshape(-1, 2)
        dst_pts = np.array([keypoints_2[m.trainIdx].pt for m in matches]).reshape(-1, 2)

        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        matches = [m for i, m in enumerate(matches) if mask[i]]
        return matches

    @staticmethod
    def ensure_unique_matches(matches: list[cv2.DMatch]) -> list[cv2.DMatch]:
        """Ensure no more than one match per keypoint.

        Args:
            matches: matches.

        Returns:
            unique matches.
        """
        unique_matches = []
        seen_query_indices, seen_train_indices = set(), set()

        for match in matches:
            if (
                match.queryIdx not in seen_query_indices
                and match.trainIdx not in seen_train_indices
            ):
                unique_matches.append(match)
                seen_query_indices.add(match.queryIdx)
                seen_train_indices.add(match.trainIdx)

        return unique_matches

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
        features: list[VisualFeature], matches: list[cv2.DMatch]
    ) -> tuple[list[VisualFeature], list[int], list[VisualFeature]]:
        """Sorts features into matched and unmatched.

        Args:
            features: visual features.

            matches: features` matches.

        Returns:
            matched and unmatched features.
        """
        matched_indices = {match.queryIdx for match in matches}
        matched_features = [features[m.queryIdx] for m in matches]
        unmatched_features = [f for i, f in enumerate(features) if i not in matched_indices]
        matched_feature_indices = [m.trainIdx for m in matches]

        return matched_features, matched_feature_indices, unmatched_features
