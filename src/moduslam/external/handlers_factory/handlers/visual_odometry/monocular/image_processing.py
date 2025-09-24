import cv2
import numpy as np
from PIL.Image import Image

from moduslam.custom_types.numpy import Matrix4x4
from moduslam.external.handlers_factory.handlers.visual_odometry.feature_detector import (
    Detector,
)
from moduslam.external.handlers_factory.handlers.visual_odometry.feature_matcher import (
    BfMatcher,
    draw_matches,
)
from moduslam.sensors_factory.configs import StereoCameraConfig


def compute_transformation(
    image1: Image, image2: Image, parameters: StereoCameraConfig
) -> Matrix4x4:
    """Computes the transformation between two images.

    Args:
        image1: first image.

        image2: second image.

        parameters: parameters to compute the transformation.

    Returns:
        SE(3) transformation.
    """
    detector = Detector(num_features=6000)
    matcher = BfMatcher()

    keypoints1, descriptors1 = detector.get_keypoints_and_descriptors(image1)
    keypoints2, descriptors2 = detector.get_keypoints_and_descriptors(image2)

    matches = matcher.get_matches(descriptors1, descriptors2)
    matches = matches[:1000]
    draw_matches(image1, image2, keypoints1, keypoints2, matches)

    q1 = np.float32([keypoints1[m.queryIdx].pt for m in matches])
    q2 = np.float32([keypoints2[m.trainIdx].pt for m in matches])

    tf = _get_transformation(
        q1,
        q2,
        parameters.camera_matrix_left,
        parameters.distortion_coefficients_left,
        parameters.camera_matrix_right,
        parameters.distortion_coefficients_right,
    )

    return tf


def _get_transformation(
    points1, points2, cam_matrix1, dist_coeffs1, cam_matrix2, dist_coeffs2
) -> Matrix4x4:
    # Convert camera matrices and distortion coefficients to numpy arrays
    cam_matrix1 = np.array(cam_matrix1)
    cam_matrix2 = np.array(cam_matrix2)
    dist_coeffs1 = np.array(dist_coeffs1)
    dist_coeffs2 = np.array(dist_coeffs2)

    # Recover pose
    _, E, R, t, mask = cv2.recoverPose(
        points1, points2, cam_matrix1, dist_coeffs1, cam_matrix2, dist_coeffs2, prob=0.99
    )

    # Adjust rotation and translation
    R = R.transpose()
    t = -np.matmul(R, t)

    # Create transformation matrix
    tf = np.eye(4)
    tf[:3, :3] = R
    tf[:3, 3] = t.flatten()

    return tf


# def _get_transformation(points1, points2, camera_matrix: list[list[float]]) -> Matrix4x4:
#     fx = camera_matrix[0][0]
#     cx = camera_matrix[0][2]
#     cy = camera_matrix[1][2]
#
#     E, mask = cv2.findEssentialMat(
#         points1, points2, focal=fx, pp=(cx, cy), method=cv2.RANSAC, prob=0.999, threshold=1
#     )
#
#     points1 = points1[mask.ravel() == 1]
#     points2 = points2[mask.ravel() == 1]
#
#     _, R, t, mask = cv2.recoverPose(E, points1, points2, focal=fx, pp=(cx, cy))
#
#     R = R.transpose()
#     t = -np.matmul(R, t)
#
#     tf = np.eye(4)
#     tf[:3, :3] = R
#     tf[:3, 3] = t.flatten()
#
#     return tf
