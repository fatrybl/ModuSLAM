import pytest

from moduslam.measurement_storage.measurements.auxiliary import FakeMeasurement
from moduslam.measurement_storage.storage import MeasurementStorage as Storage
from moduslam.utils.exceptions import ValidationError
from moduslam.utils.ordered_set import OrderedSet


def test_add_measurement():
    t = 0
    measurement = FakeMeasurement(t)
    os = OrderedSet[FakeMeasurement]()
    os.add(measurement)

    Storage.add(measurement)

    assert type(measurement) in Storage.data()
    assert measurement in Storage.data()[type(measurement)]
    assert Storage.time_range().start == Storage.time_range().stop == t
    assert Storage.empty() is False
    assert Storage.recent_measurement() == measurement
    assert Storage.data() == {FakeMeasurement: os}


def test_add_duplicate_measurement_raises_validation_error():
    t = 0
    measurement = FakeMeasurement(t)

    Storage.add(measurement)

    with pytest.raises(ValidationError):
        Storage.add(measurement)


def test_add_measurement_updates_start_and_stop_timestamps():
    t1, t2 = 0, 1
    measurement1, measurement2 = FakeMeasurement(t1), FakeMeasurement(t2)

    Storage.add(measurement1)

    assert Storage.time_range().start == t1
    assert Storage.time_range().stop == t1

    Storage.add(measurement2)

    assert Storage.time_range().start == t1
    assert Storage.time_range().stop == t2


def test_add_measurement_with_earlier_timestamp_updates_start_and_stop_timestamps():
    t1, t2 = 1, 0  # t2 is earlier than t1
    measurement1 = FakeMeasurement(t1)
    measurement2 = FakeMeasurement(t2)

    Storage.add(measurement1)

    assert Storage.time_range().start == t1
    assert Storage.time_range().stop == t1

    Storage.add(measurement2)

    assert Storage.time_range().start == t2
    assert Storage.time_range().stop == t1


def test_add_measurement_of_new_type_creates_new_ordered_set():
    t = 0
    new_measurement = FakeMeasurement(t)

    assert Storage.empty() is True

    Storage.add(new_measurement)

    assert isinstance(Storage.data()[type(new_measurement)], OrderedSet)
    assert new_measurement in Storage.data()[type(new_measurement)]


def test_add_maintains_order_in_ordered_set():
    t1, t2, t3 = 0, 1, 2
    measurement1 = FakeMeasurement(t1)
    measurement2 = FakeMeasurement(t2)
    measurement3 = FakeMeasurement(t3)

    Storage.add(measurement1)
    Storage.add(measurement2)
    Storage.add(measurement3)

    ordered_set = Storage.data()[type(measurement1)]

    assert list(ordered_set) == [measurement1, measurement2, measurement3]


def test_add_updates_recent_measurement():
    t1, t2 = 0, 2
    measurement1, measurement2 = FakeMeasurement(t1), FakeMeasurement(t2)

    Storage.add(measurement1)

    recent = Storage.recent_measurement()
    assert recent is measurement1

    Storage.add(measurement2)

    recent = Storage.recent_measurement()
    assert Storage.recent_measurement() is measurement2
