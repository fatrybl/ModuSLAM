import pytest

from src.measurement_storage.measurements.imu import ImuData
from src.utils.auxiliary_objects import zero_vector3


@pytest.fixture
def data() -> ImuData:
    """Zeroed ImuData object."""
    return ImuData(zero_vector3, zero_vector3)
