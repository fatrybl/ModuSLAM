from moduslam.bridge.preprocessors.fake_measurement_factory import find_fake_measurement
from moduslam.measurement_storage.measurements.auxiliary import (
    FakeMeasurement,
    PseudoMeasurement,
)


def test_find_fake_measurement_empty_iterable():
    assert find_fake_measurement([]) is None


def test_find_fake_measurement_no_fake_measurements():
    measurements = [PseudoMeasurement(1, 1)]
    assert find_fake_measurement(measurements) is None


def test_find_fake_measurement_equal_but_not_identical_value():
    fake = FakeMeasurement(1)
    non_fake = PseudoMeasurement(1, fake.value)
    measurements = [fake, non_fake]

    result = find_fake_measurement(measurements)

    assert result is fake


def test_find_fake_measurement_correct_cast():
    fake_measurement = FakeMeasurement(1)
    measurements = [
        PseudoMeasurement(1, "a"),
        PseudoMeasurement(2, "b"),
        fake_measurement,
    ]

    result = find_fake_measurement(measurements)

    assert result is fake_measurement
