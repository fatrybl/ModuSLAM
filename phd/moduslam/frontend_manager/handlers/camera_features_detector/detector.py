"""Extracts ORB keypoints and descriptors from images."""

from collections.abc import Iterable, Sequence

import cv2
import numpy as np
from PIL.Image import Image, fromarray
from PIL.ImageFile import ImageFile

from phd.moduslam.custom_types.numpy import Matrix3x3, MatrixMxN, VectorN
from phd.moduslam.utils.auxiliary_dataclasses import Position, VisualFeature
from phd.moduslam.utils.auxiliary_methods import matrix_to_vector_list


class KeypointDetector:

    def __init__(self, num_features: int = 500) -> None:
        self._orb = cv2.ORB.create(nfeatures=num_features, scoreType=cv2.ORB_HARRIS_SCORE)

    def get_orb_keypoints(self, image: Image) -> tuple[Sequence[cv2.KeyPoint], MatrixMxN]:
        """Gets ORB features and modified BRIEF descriptors from an image.

        Args:
            image: image to extract features from.

        Returns:
            keypoints and descriptors.
        """
        array = np.array(image, dtype=np.uint8)
        mask = np.ones(shape=array.shape, dtype=np.uint8) * 255
        keypoints, descriptors = self._orb.detectAndCompute(array, mask=mask)
        return keypoints, descriptors

    @staticmethod
    def undistort_image(image: ImageFile, camera_matrix: Matrix3x3, dist_coeffs: VectorN) -> Image:
        """Removes distortion of an image and recomputes the camera matrix.

        Args:
            image: distorted image.

            camera_matrix: original camera matrix.

            dist_coeffs: distortion coefficients.

        Returns:
            undistorted_image and new camera matrix.
        """
        # h, w = image.height, image.width
        array = np.array(image)
        # new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(
        #     camera_matrix, dist_coeffs, (w, h), 1, (w, h)
        # )

        # new_camera_matrix = new_camera_matrix.astype(np.float64)
        undistorted_array = cv2.undistort(array, camera_matrix, dist_coeffs, None, camera_matrix)
        undistorted_image = fromarray(undistorted_array)

        return undistorted_image

    @staticmethod
    def project_3d(
        depth_image: MatrixMxN, keypoints: Sequence[cv2.KeyPoint], camera_matrix: Matrix3x3
    ) -> list[Position]:
        """Convert keypoints to 3D points using a depth image and a camera matrix.

        Args:
            depth_image: Depth map.

            keypoints: sequence of keypoints.

            camera_matrix: camera intrinsic matrix.

        Returns:
            3D points.
        """
        fx = camera_matrix[0, 0]
        fy = camera_matrix[1, 1]
        cx = camera_matrix[0, 2]
        cy = camera_matrix[1, 2]

        points_3d = []

        for kp in keypoints:
            u, v = int(kp.pt[0]), int(kp.pt[1])
            z = depth_image[v, u]
            x = (u - cx) * z / fx
            y = (v - cy) * z / fy
            p = Position(x, y, z)
            points_3d.append(p)

        return points_3d

    @staticmethod
    def create_visual_features(
        keypoints: Iterable[cv2.KeyPoint], descriptors: Iterable[VectorN]
    ) -> list[VisualFeature]:
        """Creates a list of visual features from keypoints and descriptors.

        Args:
            keypoints: detected keypoints.

            descriptors: descriptors of keypoints.

        Returns:
            list of visual features.
        """
        features = []
        for key_point, descriptor in zip(keypoints, descriptors):
            feature = VisualFeature(key_point, descriptor)
            features.append(feature)
        return features

    def get_visual_features(self, image: ImageFile | Image) -> list[VisualFeature]:
        """Gets visual features from an image.

        Args:
            image: image to extract features from.

        Returns:
            list of visual features.
        """

        keypoints, descriptors = self.get_orb_keypoints(image)
        descriptors_list = matrix_to_vector_list(descriptors)
        features = self.create_visual_features(keypoints, descriptors_list)
        return features
