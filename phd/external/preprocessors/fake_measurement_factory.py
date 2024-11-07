from collections.abc import Iterable

from phd.external.objects.auxiliary_classes import FakeMeasurement
from phd.measurements.processed_measurements import Measurement


def add_fake_if_needed(
    measurements: list[Measurement], imu_measurements: list[Measurement]
) -> None:
    """Adds a fake measurement inplace to the measurements if a start of the continuous
    measurement is earlier then the 1-st measurement timestamp.

    Args:
        measurements: a sequence of measurements.

        imu_measurements: a sequence of measurements to be used for checking the start timestamp.
    """
    imu_start = imu_measurements[0].timestamp
    others_start = measurements[0].timestamp
    if imu_start < others_start:
        fake = FakeMeasurement(imu_start)
        measurements.insert(0, fake)


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
