import gtsam
import pytest


@pytest.fixture
def noise() -> gtsam.noiseModel.Isotropic:
    """GTSAM noise model with sigma = 1.0."""
    return gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
