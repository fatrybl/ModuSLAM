import logging

import gtsam

from slam.logger.logging_config import frontend_manager_logger

logger = logging.getLogger(frontend_manager_logger)


def pose_isotropic_noise_model(variance: float) -> gtsam.noiseModel.Isotropic.Variance:
    """Isotropic Gaussian noise model for pose: [x, y, z, roll, pitch, yaw].

    Args:
        variance: float representing the standard deviation of the noise.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Isotropic.Variance(6, variance)
    return noise


def pose_diagonal_noise_model(
    noise_variance: tuple[float, float, float, float, float, float],
) -> gtsam.noiseModel.Diagonal.Variances:
    """Diagonal Gaussian noise model for pose: [x, y, z, roll, pitch, yaw].

    Args:
        noise_variance: tuple of 6 floats representing the variances of the noise.

    Returns:
        gtsam noise model.
    """

    noise = gtsam.noiseModel.Diagonal.Variances(noise_variance)
    return noise
