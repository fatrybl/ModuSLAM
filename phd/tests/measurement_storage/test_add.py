import pytest

from phd.measurements.auxiliary_classes import FakeMeasurement
from phd.measurements.storage import MeasurementStorage
from phd.moduslam.utils.exceptions import ValidationError
from phd.moduslam.utils.ordered_set import OrderedSet


def test_add_measurement():
    t = 0
    storage = MeasurementStorage()
    measurement = FakeMeasurement(t)
    os = OrderedSet[FakeMeasurement]()
    os.add(measurement)

    storage.add(measurement)

    assert measurement in storage
    assert storage.time_range.start == storage.time_range.stop == t
    assert storage.empty is False
    assert storage.recent_measurement == measurement
    assert storage.data == {FakeMeasurement: os}


def test_add_duplicate_measurement_raises_validation_error():
    t = 0
    storage = MeasurementStorage()
    measurement = FakeMeasurement(t)

    storage.add(measurement)

    with pytest.raises(ValidationError):
        storage.add(measurement)


def test_add_measurement_updates_start_and_stop_timestamps():
    t1, t2 = 0, 1
    storage = MeasurementStorage()
    measurement1, measurement2 = FakeMeasurement(t1), FakeMeasurement(t2)

    storage.add(measurement1)
    assert storage.time_range.start == t1
    assert storage.time_range.stop == t1

    storage.add(measurement2)
    assert storage.time_range.start == t1
    assert storage.time_range.stop == t2


def test_add_measurement_with_earlier_timestamp_updates_start_and_stop_timestamps():
    t1, t2 = 1, 0  # t2 is earlier than t1
    storage = MeasurementStorage()
    measurement1 = FakeMeasurement(t1)
    measurement2 = FakeMeasurement(t2)

    storage.add(measurement1)
    assert storage.time_range.start == t1
    assert storage.time_range.stop == t1

    storage.add(measurement2)
    assert storage.time_range.start == t2
    assert storage.time_range.stop == t1


def test_add_measurement_of_new_type_creates_new_ordered_set():
    t = 0
    storage = MeasurementStorage()
    new_measurement = FakeMeasurement(t)

    assert storage.empty is True

    storage.add(new_measurement)

    assert isinstance(storage.data[type(new_measurement)], OrderedSet)
    assert new_measurement in storage.data[type(new_measurement)]


def test_add_maintains_order_in_ordered_set():
    t1, t2, t3 = 0, 1, 2
    storage = MeasurementStorage()
    measurement1 = FakeMeasurement(t1)
    measurement2 = FakeMeasurement(t2)
    measurement3 = FakeMeasurement(t3)

    storage.add(measurement1)
    storage.add(measurement2)
    storage.add(measurement3)

    ordered_set = storage.data[type(measurement1)]

    assert list(ordered_set) == [measurement1, measurement2, measurement3]


def test_add_updates_recent_measurement():
    t1, t2 = 0, 2
    storage = MeasurementStorage()
    measurement1, measurement2 = FakeMeasurement(t1), FakeMeasurement(t2)

    storage.add(measurement1)
    assert storage.recent_measurement == measurement1

    storage.add(measurement2)
    assert storage.recent_measurement == measurement2
