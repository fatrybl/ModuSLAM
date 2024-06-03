from collections.abc import Sequence

import cv2
import numpy as np
from PIL.Image import Image

from moduslam.frontend_manager.handlers.visual_odometry.depth_estimator import (
    DepthEstimator,
)
from moduslam.utils.numpy_types import (
    Matrix3x3,
    Matrix4x4,
    MatrixMxN,
    MatrixNx2,
    MatrixNx3,
    VectorN,
)


def get_orb_features(image: MatrixMxN) -> tuple[Sequence[cv2.KeyPoint], np.ndarray]:
    """Gets ORB features and modified BRIEF descriptors from an image.

    Args:
        image: image to extract features from.

    Returns:
        keypoints: keypoints found in the image.
        descriptors: descriptors for the keypoints.
    """
    orb = cv2.ORB.create()
    mask = np.ones(image.shape[:2], dtype=np.uint8) * 255
    keypoints, descriptors = orb.detectAndCompute(image, mask=mask)
    return keypoints, descriptors


def match_keypoints(descriptors1: MatrixMxN, descriptors2: MatrixMxN) -> Sequence[cv2.DMatch]:
    """Matches keypoints between two sets of descriptors.

    Args:
        descriptors1: first set of descriptors.
        descriptors2: second set of descriptors.

    Returns:
        matches: matches between the two sets of descriptors.
    """
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    return matches


def get_points_and_pixels(
    depth_1: MatrixMxN,
    depth_2: MatrixMxN,
    keypoints1: Sequence[cv2.KeyPoint],
    keypoints2: Sequence[cv2.KeyPoint],
    matches: Sequence[cv2.DMatch],
    camera_matrix: Matrix3x3,
) -> tuple[MatrixNx3, MatrixNx2]:
    """Gets 3D points and corresponding pixels for matched features of two images.

    Args:
        depth_1: depth map of the first image.
        depth_2: depth map of the second image.
        keypoints1: keypoints from the first image.
        keypoints2: keypoints from the second image.
        matches: matches between the keypoints.
        camera_matrix: camera matrix.

    Returns:
        points: 3D points.
        pixels: corresponding pixels.
    """
    points = np.empty((0, 3), dtype=np.float64)
    pixels = np.empty((0, 2), dtype=np.float64)

    for match in matches:
        u1, v1 = keypoints1[match.queryIdx].pt
        u2, v2 = keypoints2[match.trainIdx].pt

        u1, v1, u2, v2 = map(int, (u1, v1, u2, v2))

        if (
            0 <= u1 < depth_1.shape[1]
            and 0 <= v1 < depth_1.shape[0]
            and 0 <= u2 < depth_2.shape[1]
            and 0 <= v2 < depth_2.shape[0]
        ):
            d = depth_1[v1, u1]
            x, y, z = pixel_to_xyz(pixel=(u1, v1), depth=d, camera_matrix=camera_matrix)

            points = np.vstack((points, [x, y, z]))
            pixels = np.vstack((pixels, [u2, v2]))

    return points, pixels


def compute_transformation(
    points: MatrixNx3, pixels: MatrixNx3, camera_matrix: Matrix3x3, dist_coefficients: VectorN
) -> Matrix4x4:
    """Computes transformation between two sets of points and pixels.

    Args:
        points: 3D points.
        pixels: corresponding pixels.
        camera_matrix: camera matrix.
        dist_coefficients: distortion coefficients.

    Returns:
        SE(3) transformation matrix.
    """

    _, rvec, tvec, _ = cv2.solvePnPRansac(points, pixels, camera_matrix, dist_coefficients)

    r, _ = cv2.Rodrigues(rvec)
    tf = np.eye(4)
    tf[:3, :3] = r
    tf[:3, 3] = tvec.flatten()
    return tf


def pointcloud_from_image(image: Image, camera_matrix: Matrix3x3) -> MatrixNx3:
    """Creates a pointcloud from the given image.

    Args:
        image: image.

        camera_matrix: camera matrix.

    Returns:
        Pointcloud array [N, 3].
    """
    depth_estimator = DepthEstimator()
    depth_map = depth_estimator.estimate_depth(image)

    d_height, d_width = depth_map.shape
    height, width = d_height, d_width
    pointcloud = np.zeros((height * width, 3))

    for v in range(height):
        for u in range(width):
            d = depth_map[v, u]
            x, y, z = pixel_to_xyz(pixel=(u, v), depth=d, camera_matrix=camera_matrix)
            pointcloud[v * width + u] = [x, y, z]

    return pointcloud


def pixel_to_xyz(
    pixel: tuple[int, int], depth: float, camera_matrix: Matrix3x3
) -> tuple[float, float, float]:
    """Converts pixels to 3D points using the depth map.

    Args:
        pixel: pixel coordinates (u, v).

        depth: depth value.

        camera_matrix: camera matrix.

    Returns:
        3D points.
    """
    fx = camera_matrix[0][0]
    fy = camera_matrix[1][1]
    cx = camera_matrix[0][2]
    cy = camera_matrix[1][2]

    u, v = pixel
    z = depth
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy

    return x, y, z
