from collections.abc import Iterable

from phd.external.objects.measurements import (
    ContinuousMeasurement,
    FakeMeasurement,
    Measurement,
)


def add_fake_if_needed(
    continuous_measurement: ContinuousMeasurement, measurements: list[Measurement]
) -> None:
    t1 = continuous_measurement.time_range.start
    t2 = measurements[0].timestamp
    if t1 < t2:
        fake = create_fake(continuous_measurement)
        measurements.insert(0, fake)


def create_fake(measurement: ContinuousMeasurement) -> FakeMeasurement:
    """Creates a fake measurement.

    Args:
        measurement: measurement to be used for fake measurement.

    Returns:
        fake measurement.
    """
    t = measurement.time_range.start
    return FakeMeasurement(t)


def find_fake_measurement(measurements: Iterable[Measurement]) -> FakeMeasurement | None:
    """Finds the 1-st fake measurement in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        the 1-st fake measurement if found or None.
    """
    for m in measurements:
        if m.value == FakeMeasurement.fake_value and isinstance(m, FakeMeasurement):
            return m
    return None
