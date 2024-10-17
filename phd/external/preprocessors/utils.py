from collections.abc import Iterable

from phd.external.objects.measurements import ContinuousMeasurement, Measurement


def find_continuous_measurement(
    measurements: Iterable[Measurement],
) -> ContinuousMeasurement | None:
    """Finds the 1-st continuous measurement in the sequence.

    Args:
        measurements: sequence of measurements.

    Returns:
        1-st continuous measurement if found or None.
    """
    for m in measurements:
        if isinstance(m, ContinuousMeasurement):
            return m
    return None
