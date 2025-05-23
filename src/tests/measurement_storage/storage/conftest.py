import pytest

from src.measurement_storage.storage import MeasurementStorage


@pytest.fixture(autouse=True, scope="function")
def clean_storage():
    MeasurementStorage.clear()
