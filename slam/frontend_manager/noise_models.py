import logging

import gtsam

logger = logging.getLogger(__name__)


def get_noise_model_method(noise_model_name: str):
    """
    TODO: maybe remove ?
    """
    noise_models: list[str] = [
        gtsam.noiseModel.Diagonal.__name__,
        gtsam.noiseModel.Isotropic.__name__,
        gtsam.noiseModel.Unit.__name__,
        gtsam.noiseModel.Constrained.__name__,
        gtsam.noiseModel.Robust.__name__,
    ]
    match noise_model_name:
        case gtsam.noiseModel.Diagonal.__name__:
            return gtsam.noiseModel.Diagonal.Sigmas
        case gtsam.noiseModel.Isotropic.__name__:
            return gtsam.noiseModel.Isotropic.Sigmas
        case gtsam.noiseModel.Unit.__name__:
            return gtsam.noiseModel.Unit.Sigma
        case gtsam.noiseModel.Constrained.__name__:
            return gtsam.noiseModel.Constrained.Sigmas
        case gtsam.noiseModel.Robust.__name__:
            return gtsam.noiseModel.Robust.Create

        case _:
            msg = f"Invalid noise model: {noise_model_name}. Valid noise models: {noise_models}"
            raise ValueError(msg)


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
