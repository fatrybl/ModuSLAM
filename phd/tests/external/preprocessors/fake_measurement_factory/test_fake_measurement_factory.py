from phd.external.objects.measurements import CoreMeasurement, FakeMeasurement
from phd.external.preprocessors.fake_measurement_factory import find_fake_measurement


def test_find_fake_measurement_empty_iterable():
    assert find_fake_measurement([]) is None


def test_find_fake_measurement_no_fake_measurements():
    measurements = [CoreMeasurement(1, 1)]
    assert find_fake_measurement(measurements) is None


def test_find_fake_measurement_equal_but_not_identical_value():
    measurements = [CoreMeasurement(1, FakeMeasurement.fake_value), FakeMeasurement(1)]
    result = find_fake_measurement(measurements)
    assert isinstance(result, FakeMeasurement)
    assert result.value == FakeMeasurement.fake_value


def test_find_fake_measurement_correct_cast():
    fake_measurement = FakeMeasurement(1)
    measurements = [CoreMeasurement(1, "a"), CoreMeasurement(2, "b"), fake_measurement]
    result = find_fake_measurement(measurements)
    assert result is not None
    assert isinstance(result, FakeMeasurement)
    assert result.value == FakeMeasurement.fake_value
    assert result is fake_measurement
