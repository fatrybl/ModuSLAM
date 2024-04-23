import logging
from collections.abc import Collection

import gtsam
import numpy as np

logger = logging.getLogger(__name__)


def get_noise_model_method(noise_model_name: str):
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


def pose_diagonal_noise_model(
    values: Collection[float],
) -> gtsam.noiseModel.Diagonal.Sigmas:
    """Diagonal Gaussian noise model for pose: [x, y, z, roll, pitch, yaw].

    Args:
        values (Collection[float]): measurement noise sigmas: [x, y, z, roll, pitch, yaw].

    Returns:
        noise model (gtsam.noiseModel.Diagonal.Sigmas).
    """
    num_values: int = len(values)
    if num_values != 6:
        msg = f"Expected 6 values: [x, y, z, roll, pitch, yaw]. Got: {num_values}"
        logger.critical(msg)
        raise ValueError(msg)
    else:
        values = np.array(values, dtype=float)
        return gtsam.noiseModel.Diagonal.Sigmas(values)
