import gtsam
import numpy as np

from phd.moduslam.custom_types.aliases import Matrix3x3, Vector3
from phd.moduslam.custom_types.numpy import Matrix6x6


def create_block_diagonal_matrix(block1: Matrix3x3, block2: Matrix3x3) -> Matrix6x6:
    """Block diagonal matrix with two 3x3 blocks.

    Args:
        block1: 3x3 block matrix.

        block2: 3x3 block matrix.

    Returns:
        Block diagonal numpy matrix.
    """
    position_cov_matrix = np.array(block1)
    orientation_cov_matrix = np.array(block2)

    block_matrix = np.block(
        [[position_cov_matrix, np.zeros((3, 3))], [np.zeros((3, 3)), orientation_cov_matrix]]
    )
    return block_matrix


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
    bloc_matrix = create_block_diagonal_matrix(position_covariance, orientation_covariance)
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
