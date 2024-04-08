"""Tests for MeasurementStorage class."""

import pytest

from slam.data_manager.factory.element import Element
from slam.data_manager.factory.element import Measurement as RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.utils.ordered_set import OrderedSet
from tests.frontend_manager.conftest import measurement, sensor  # noqa: F401, F811


@pytest.fixture
def elements(sensor) -> tuple[Element, ...]:
    loc = Location()
    m1 = RawMeasurement(sensor=sensor, values=(1, 2, 3))
    m2 = RawMeasurement(sensor=sensor, values=(4, 5, 6))
    el1 = Element(timestamp=0, location=loc, measurement=m1)
    el2 = Element(timestamp=1, location=loc, measurement=m2)
    return el1, el2


class TestMeasurementStorage:
    def test_measurement_hashable(self, measurement):
        try:
            hash(measurement)
        except TypeError:
            pytest.fail("Measurement object is not hashable.")
        else:
            assert True

    def test_add_measurement(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        assert measurement in storage.data[measurement.handler]

    def test_add_data(self, measurement):
        storage = MeasurementStorage()
        data = {measurement.handler: OrderedSet([measurement])}
        storage.add(data)
        assert measurement in storage.data[measurement.handler]

    def test_remove(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        storage.remove(measurement)
        assert storage.is_empty

    def test_clear(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        storage.clear()
        assert storage.is_empty

    def test_recent_measurement(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        assert storage.recent_measurement == measurement

    def test_time_range(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        assert storage.time_range == measurement.time_range
