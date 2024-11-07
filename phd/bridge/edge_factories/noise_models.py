import gtsam

from phd.moduslam.custom_types.aliases import Matrix3x3, Vector3, Vector6


def position_noise_model(covariance: Matrix3x3) -> gtsam.noiseModel.Gaussian.Covariance:
    """Gaussian noise model for position: [x, y, z].

    Args:
        covariance: 3x3 covariance matrix of the noise.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Gaussian.Covariance(covariance)
    return noise


def position_diagonal_noise_model(noise_variances: Vector3) -> gtsam.noiseModel.Diagonal.Variances:
    """Diagonal Gaussian noise model for position: [x, y, z].

    Args:
        noise_variances: tuple of 3 floats representing the variances of the noise.

    Returns:
        gtsam noise model.
    """
    noise = gtsam.noiseModel.Diagonal.Variances(noise_variances)
    return noise


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
    noise_variances: Vector6,
) -> gtsam.noiseModel.Diagonal.Variances:
    """Diagonal Gaussian noise model for pose: [x, y, z, roll, pitch, yaw].

    Args:
        noise_variances: tuple of 6 floats representing the variances of the noise.

    Returns:
        gtsam noise model.
    """

    noise = gtsam.noiseModel.Diagonal.Variances(noise_variances)
    return noise


def pixel_diagonal_noise_model(
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
