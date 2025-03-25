"""Extracts ORB keypoints and descriptors from images."""

from collections.abc import Sequence

import cv2
import numpy as np
from PIL.Image import Image

from src.custom_types.numpy import MatrixMxN


class Detector:
    """Extracts ORB keypoints and descriptors from images."""

    def __init__(self, num_features: int = 3000) -> None:
        self._detector = cv2.ORB.create(nfeatures=num_features)

    def get_keypoints_and_descriptors(
        self, image: Image
    ) -> tuple[Sequence[cv2.KeyPoint], MatrixMxN]:
        """Gets ORB features and modified BRIEF descriptors from an image.

        Args:
            image: image to extract features from.

        Returns:
            key points and descriptors.
        """
        array = np.array(image)
        mask = np.ones(shape=array.shape, dtype=np.uint8) * 255
        keypoints, descriptors = self._detector.detectAndCompute(array, mask=mask)
        return keypoints, descriptors
