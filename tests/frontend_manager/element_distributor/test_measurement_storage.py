"""Tests for MeasurementStorage class."""

import pytest

from slam.data_manager.factory.element import Element, RawMeasurement
from slam.data_manager.factory.locations import Location
from slam.frontend_manager.measurement_storage import Measurement, MeasurementStorage
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.utils.auxiliary_dataclasses import TimeRange
from tests.frontend_manager.conftest import (  # noqa: F401, F811
    BasicTestHandler,
    element,
    handler,
    measurement,
    sensor,
)


@pytest.fixture
def elements(sensor: Sensor) -> tuple[Element, ...]:
    loc = Location()
    m1 = RawMeasurement(sensor=sensor, values=(1, 2, 3))
    m2 = RawMeasurement(sensor=sensor, values=(4, 5, 6))
    el1 = Element(timestamp=0, location=loc, measurement=m1)
    el2 = Element(timestamp=1, location=loc, measurement=m2)
    return el1, el2


@pytest.fixture
def measurements(handler: BasicTestHandler, element: Element):
    m1 = Measurement(
        time_range=TimeRange(element.timestamp, element.timestamp),
        values=(1, 2, 3),
        handler=handler,
        elements=(element,),
        noise_covariance=(1, 1, 1),
    )
    m2 = Measurement(
        time_range=TimeRange(element.timestamp + 1, element.timestamp + 1),
        values=(1, 2, 3),
        handler=handler,
        elements=(element,),
        noise_covariance=(1, 1, 1),
    )
    m3 = Measurement(
        time_range=TimeRange(element.timestamp + 2, element.timestamp + 2),
        values=(1, 2, 3),
        handler=handler,
        elements=(element,),
        noise_covariance=(1, 1, 1),
    )

    m4 = Measurement(
        time_range=TimeRange(element.timestamp, element.timestamp + 1),
        values=(1, 2, 3),
        handler=handler,
        elements=(element,),
        noise_covariance=(1, 1, 1),
    )

    return m1, m2, m3, m4


class TestMeasurementStorage:
    def test_measurement_hashable(self, measurement):
        try:
            hash(measurement)
        except TypeError:
            pytest.fail("Measurement object is not hashable.")
        else:
            assert True

    def test_add(self, measurement: Measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        assert measurement in storage.data[measurement.handler]

    def test_add_same(self, measurement: Measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        storage.add(measurement)
        assert len(storage.data[measurement.handler]) == 1

    def test_add_multiples(self, measurements: tuple[Measurement, ...]):
        storage = MeasurementStorage()
        storage.add(measurements)
        assert all(m in storage.data[m.handler] for m in measurements)
        assert storage.recent_measurement == measurements[2]

    def test_remove(self, measurement: Measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        storage.remove(measurement)
        assert storage.empty

    def test_remove_nonexistent(self, measurement: Measurement):
        storage = MeasurementStorage()
        with pytest.raises(KeyError):
            storage.remove(measurement)

    def test_remove_multiples(self, measurements: tuple[Measurement, ...]):
        storage = MeasurementStorage()
        storage.add(measurements)
        storage.remove(measurements)
        assert storage.empty

    def test_clear(self, measurement: Measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        storage.clear()
        assert storage.empty

    def test_recent_measurement(self, measurement: Measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        assert storage.recent_measurement == measurement

    def test_time_range(self, measurements: tuple[Measurement, ...]):
        storage = MeasurementStorage()
        storage.add(measurements)

        time_range = TimeRange(
            start=measurements[0].time_range.start,
            stop=measurements[2].time_range.stop,
        )
        assert storage.time_range == time_range
