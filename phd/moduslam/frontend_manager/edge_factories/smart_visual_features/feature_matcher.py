import logging
from collections.abc import Sequence

import cv2
import numpy as np

from moduslam.logger.logging_config import frontend_manager

logger = logging.getLogger(frontend_manager)


class FeatureMatcher:
    def __init__(self):
        self._bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self._min_required_matches: int = 4
        self._ransac_reproj_threshold: float = 1.0
        self._num_matches: int | None = None

    @staticmethod
    def reshape_array(arr: np.ndarray) -> np.ndarray:
        if arr.ndim == 2:
            return arr
        elif arr.ndim == 1:
            return arr.reshape(1, 32)
        elif arr.ndim == 3:
            return arr.squeeze()
        else:
            raise ValueError("Unsupported array shape")

    def find_matches(
        self, descriptors_1: np.ndarray, descriptors_2: np.ndarray
    ) -> Sequence[cv2.DMatch]:
        """Find matches between two sets of descriptors using a brute-force matcher.

        Args:
            descriptors_1: descriptors of the first set.

            descriptors_2: descriptors of the second set.

        Returns:
            matches.
        """
        descriptors_1 = self.reshape_array(descriptors_1)
        descriptors_2 = self.reshape_array(descriptors_2)

        matches = self._bf.match(descriptors_1, descriptors_2)
        if self._num_matches:
            return matches[: self._num_matches]
        else:
            return matches

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
            msg = f"Number of matches is less than the required minimum of {self._min_required_matches} for RANSAC."
            logger.error(msg)
            return []

        src_pts = np.array([keypoints_1[m.queryIdx].pt for m in matches]).reshape(-1, 2)
        dst_pts = np.array([keypoints_2[m.trainIdx].pt for m in matches]).reshape(-1, 2)

        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, self._ransac_reproj_threshold)

        matches = [m for i, m in enumerate(matches) if mask[i]]

        if len(matches) == 0:
            logger.warning("Number of matches after RANSAC is 0.")

        return matches

    @staticmethod
    def filter_with_ration_test(
        matches: Sequence[cv2.DMatch], ratio: float = 0.8
    ) -> list[cv2.DMatch]:
        """Filter matches with ratio test.

        Args:
            matches: matches.

            ratio: ratio threshold.

        Returns:
            filtered matches.
        """
        if len(matches) < 2:
            logger.warning("Number of matches is less than 2 for Lowe's ratio test.")
            return []

        matches = sorted(matches, key=lambda x: x.distance)
        good_matches = []
        for m, n in zip(matches, matches[1:]):
            if m.distance < ratio * n.distance:
                good_matches.append(m)

        return good_matches
