import gtsam
import numpy as np

from phd.moduslam.custom_types.aliases import Matrix3x3, Vector3


def covariance3x3_noise_model(covariance: Matrix3x3) -> gtsam.noiseModel.Gaussian.Covariance:
    """Gaussian noise model with 3x3 covariance matrix.

    Args:
        covariance: 3x3 covariance matrix of the noise.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Gaussian.Covariance(covariance)
    return noise


def diagonal3x3_noise_model(noise_variances: Vector3) -> gtsam.noiseModel.Diagonal.Variances:
    """Diagonal Gaussian noise model for 3D vector.

    Args:
        noise_variances: tuple of 3 floats representing the variances of the noise.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Diagonal.Variances(noise_variances)
    return noise


def se3_isotropic_noise_model(variance: float) -> gtsam.noiseModel.Isotropic.Variance:
    """Isotropic Gaussian noise model for pose: [x, y, z, roll, pitch, yaw].

    Args:
        variance: float representing the standard deviation of the noise.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Isotropic.Variance(6, variance)
    return noise


def pose_block_diagonal_noise_model(
    position_covariance: Matrix3x3, orientation_covariance: Matrix3x3
) -> gtsam.noiseModel.Diagonal.Covariance:
    """Block diagonal covariance noise model for SE(3) Pose.

    Args:
        position_covariance: 3x3 covariance matrix of the position noise.

        orientation_covariance: 3x3 covariance matrix of the orientation noise.

    Returns:
        gtsam noise model.
    """
    position_cov_matrix = np.array(position_covariance)
    orientation_cov_matrix = np.array(orientation_covariance)

    bloc_matrix = np.block(
        [[position_cov_matrix, np.zeros((3, 3))], [np.zeros((3, 3)), orientation_cov_matrix]]
    )

    noise = gtsam.noiseModel.Diagonal.Covariance(bloc_matrix)
    return noise


def diagonal2x2_noise_model(
    noise_variances: tuple[float, float]
) -> gtsam.noiseModel.Diagonal.Variances:
    """Diagonal Gaussian noise model for pixel: [u, v].

    Args:
        noise_variances: tuple of 2 floats representing the variances of the noise.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Diagonal.Variances(noise_variances)
    return noise
