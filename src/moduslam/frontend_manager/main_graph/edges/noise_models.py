import gtsam
import numpy as np

from moduslam.custom_types.aliases import Matrix3x3, Vector3, Vector6, VectorN
from moduslam.custom_types.numpy import Matrix6x6


def block_diagonal_matrix_6x6(block1: Matrix3x3, block2: Matrix3x3) -> Matrix6x6:
    """Numpy block-diagonal matrix with two 3x3 blocks.

    Args:
        block1: 3x3 block matrix.

        block2: 3x3 block matrix.

    Returns:
        numpy block-diagonal matrix.
    """
    zero_block = np.zeros((3, 3))
    array1, array2 = np.array(block1), np.array(block2)

    return np.block(
        [
            [array1, zero_block],
            [zero_block, array2],
        ]
    )


def covariance3x3_noise_model(covariance: Matrix3x3) -> gtsam.noiseModel.Gaussian.Covariance:
    """Gaussian noise model with 3x3 covariance matrix.

    Args:
        covariance: noise covariance matrix.

    Returns:
        gtsam noise model.
    """
    array = np.array(covariance)
    noise = gtsam.noiseModel.Gaussian.Covariance(array)
    return noise


def diagonal3x3_noise_model(variances: Vector3) -> gtsam.noiseModel.Diagonal.Variances:
    """Diagonal Gaussian noise model for 3D vector.

    Args:
        variances: noise variance vector.

    Returns:
        gtsam noise model.
    """
    array = np.array(variances)
    noise = gtsam.noiseModel.Diagonal.Variances(array)
    return noise


def huber_diagonal_noise_model(
    variances: VectorN, threshold: float
) -> gtsam.noiseModel.Diagonal.Variances:
    """Diagonal Gaussian noise model for N dimensional vector.

    Args:
        variances: noise variance vector.

        threshold: Huber loss threshold.

    Returns:
        gtsam noise model.
    """
    array = np.array(variances)
    base = gtsam.noiseModel.Diagonal.Variances(array)
    loss = gtsam.noiseModel.mEstimator.Huber(threshold)
    robust = gtsam.noiseModel.Robust.Create(loss, base)
    return robust


def se3_isotropic_noise_model(variance: float) -> gtsam.noiseModel.Isotropic.Variance:
    """Isotropic Gaussian noise model for pose: [x, y, z, roll, pitch, yaw].

    Args:
        variance: noise variance scalar.

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
    matrix = block_diagonal_matrix_6x6(orientation_covariance, position_covariance)
    noise = gtsam.noiseModel.Gaussian.Covariance(matrix)
    return noise


def diagonal2x2_noise_model(variance: tuple[float, float]) -> gtsam.noiseModel.Diagonal.Sigmas:
    """Diagonal Gaussian noise model in 2D: [u, v].

    Args:
        variance: noise variance vector.

    Returns:
        gtsam noise model.
    """
    array = np.array(variance)
    noise = gtsam.noiseModel.Diagonal.Sigmas(array)
    return noise


def isotropic_3d_noise_model(variance: float) -> gtsam.noiseModel.Isotropic.Variance:
    """Isotropic Gaussian noise model for 3D vector.

    Args:
        variance: noise variance scalar.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Isotropic.Variance(3, variance)
    return noise


def isotropic_n_dim(noise_dim: int, variance: float) -> gtsam.noiseModel.Isotropic.Variance:
    """Isotropic Gaussian noise model for n-dimensional vector.

    Args:
        noise_dim: dimension of the noise vector.

        variance: noise variance scalar.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Isotropic.Variance(noise_dim, variance)
    return noise


def variance_6d(variance: Vector6) -> gtsam.noiseModel.Diagonal.Variances:
    """Diagonal Gaussian noise model for 6D vector.

    Args:
        variance: noise variance vector.

    Returns:
        gtsam noise model.
    """
    array = np.array(variance)
    noise = gtsam.noiseModel.Diagonal.Variances(array)
    return noise
