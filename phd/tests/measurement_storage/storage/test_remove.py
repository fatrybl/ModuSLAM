import pytest

from phd.measurement_storage.measurements.auxiliary import FakeMeasurement
from phd.measurement_storage.storage import MeasurementStorage as Storage
from phd.utils.exceptions import EmptyStorageError, ValidationError
from phd.utils.ordered_set import OrderedSet


class DifferentFake(FakeMeasurement):
    pass


def test_remove_measurement():
    t = 0
    measurement = FakeMeasurement(t)

    Storage.add(measurement)
    Storage.remove(measurement)

    assert measurement not in Storage.data()
    assert Storage.empty() is True
    assert Storage.data() == {}

    with pytest.raises(EmptyStorageError):
        _ = Storage.time_range()

    with pytest.raises(EmptyStorageError):
        _ = Storage.recent_measurement()


def test_remove_nonexistent_measurement_raises_validation_error():
    measurement = FakeMeasurement(0)

    with pytest.raises(ValidationError):
        Storage.remove(measurement)


def test_remove_updates_recent_measurement_correctly():
    t1, t2 = 1, 2
    measurement1, measurement2 = FakeMeasurement(t1), FakeMeasurement(t2)
    os = OrderedSet[FakeMeasurement]()
    os.add(measurement1)

    Storage.add(measurement1)
    Storage.add(measurement2)

    assert Storage.recent_measurement() == measurement2

    Storage.remove(measurement2)

    assert Storage.recent_measurement() == measurement1

    assert Storage.empty() is False
    assert Storage.data() == {FakeMeasurement: os}


def test_remove_last_measurement_of_type():
    measurement1, measurement2 = FakeMeasurement(1), FakeMeasurement(2)

    Storage.add(measurement1)
    Storage.add(measurement2)

    Storage.remove(measurement1)
    Storage.remove(measurement2)

    assert type(measurement1) not in Storage.data()
    assert type(measurement2) not in Storage.data()
    assert Storage.empty() is True
    assert Storage.data() == {}


def test_remove_nonexistent_type_does_not_alter_storage():
    measurement1, measurement2 = FakeMeasurement(0), DifferentFake(0)

    Storage.add(measurement1)

    with pytest.raises(ValidationError):
        Storage.remove(measurement2)

    assert Storage.empty() is False
    assert type(measurement1) in Storage.data()
    assert measurement1 in Storage.data()[type(measurement1)]
    assert type(measurement2) not in Storage.data()
    assert Storage.recent_measurement() is measurement1
