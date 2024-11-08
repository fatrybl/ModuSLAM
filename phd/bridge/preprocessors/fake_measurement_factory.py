from collections.abc import Iterable

from phd.bridge.objects.auxiliary_classes import FakeMeasurement
from phd.measurements.processed_measurements import Measurement


def add_fake_measurement(list_to_add: list[Measurement], timestamp: int) -> None:
    """Adds a fake measurement inplace based on the condition.

    Args:
        list_to_add: a list of measurements to add a fake in.

        timestamp: timestamp of the fake measurement.
    """
    t1 = list_to_add[0].timestamp
    if timestamp < t1:
        list_to_add.insert(0, FakeMeasurement(timestamp))


def find_fake_measurement(measurements: Iterable[Measurement]) -> FakeMeasurement | None:
    """Finds the 1-st fake measurement in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        the 1-st fake measurement if found or None.
    """
    for m in measurements:
        if isinstance(m, FakeMeasurement):
            return m
    return None
