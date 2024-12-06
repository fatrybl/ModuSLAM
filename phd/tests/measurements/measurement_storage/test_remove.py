import pytest

from phd.measurements.auxiliary_classes import FakeMeasurement
from phd.measurements.storage import MeasurementStorage
from phd.moduslam.utils.exceptions import EmptyStorageError, ValidationError
from phd.moduslam.utils.ordered_set import OrderedSet


def test_remove_measurement():
    t = 0
    storage = MeasurementStorage()
    measurement = FakeMeasurement(t)

    storage.add(measurement)
    storage.remove(measurement)

    assert measurement not in storage
    assert storage.empty is True
    assert storage.data == {}

    with pytest.raises(EmptyStorageError):
        _ = storage.time_range

    with pytest.raises(EmptyStorageError):
        _ = storage.recent_measurement


def test_remove_nonexistent_measurement_raises_validation_error():
    storage = MeasurementStorage()
    measurement = FakeMeasurement(0)

    with pytest.raises(ValidationError):
        storage.remove(measurement)


def test_remove_updates_recent_measurement_correctly():
    t1, t2 = 1, 2
    measurement1, measurement2 = FakeMeasurement(t1), FakeMeasurement(t2)
    storage = MeasurementStorage()
    os = OrderedSet[FakeMeasurement]()
    os.add(measurement1)

    storage.add(measurement1)
    storage.add(measurement2)

    assert storage.recent_measurement == measurement2

    storage.remove(measurement2)

    assert storage.recent_measurement == measurement1

    assert storage.empty is False
    assert storage.data == {FakeMeasurement: os}


def test_remove_nonexistent_type_does_not_alter_storage():
    storage = MeasurementStorage()
    measurement1 = FakeMeasurement(1)

    storage.add(measurement1)

    class DifferentFakeMeasurement(FakeMeasurement):
        pass

    different_measurement = DifferentFakeMeasurement(2)

    with pytest.raises(ValidationError):
        storage.remove(different_measurement)

    # Ensure the storage still contains the original measurement
    assert storage.empty is False
    assert measurement1 in storage
    assert different_measurement not in storage
    assert storage.recent_measurement == measurement1


def test_remove_last_measurement_of_type():
    storage = MeasurementStorage()
    measurement1, measurement2 = FakeMeasurement(1), FakeMeasurement(2)

    storage.add(measurement1)
    storage.add(measurement2)

    storage.remove(measurement1)
    storage.remove(measurement2)

    assert type(measurement1) not in storage.data
    assert type(measurement2) not in storage.data
    assert storage.empty is True
    assert storage.data == {}
