from collections.abc import Iterable

from phd.external.objects.measurements import Measurement, Odometry, SplitOdometry


def remove_odometry(measurements: list[Measurement]) -> list[Measurement]:
    """Removes odometry measurements from the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        measurements without odometry measurements.
    """
    return [m for m in measurements if not isinstance(m, Odometry)]


def find_and_split(measurements: Iterable[Measurement]) -> list[SplitOdometry] | None:
    """Finds and splits odometry measurements in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        odometry measurements if found or None.
    """
    odometry_measurements = find_odometry_measurements(measurements)
    if odometry_measurements:
        return split_multiple(odometry_measurements)
    return None


def find_odometry_measurements(measurements: Iterable[Measurement]) -> list[Odometry]:
    """Finds all odometry measurements in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        odometry measurements.
    """
    odometry_measurements = []
    for m in measurements:
        if isinstance(m, Odometry):
            odometry_measurements.append(m)

    return odometry_measurements


def split_one(measurement: Odometry) -> tuple[SplitOdometry, SplitOdometry]:
    """Splits odometry-based parent measurement into 2 children measurements with the
    same value but different timestamps.

    Args:
        measurement: parent measurement to split.

    Returns:
        2 children measurements.
    """
    m1 = SplitOdometry(measurement.time_range.start, "-" + measurement.value, measurement)
    m2 = SplitOdometry(measurement.time_range.stop, measurement.value, measurement)
    return m1, m2


def split_multiple(measurements: Iterable[Odometry]) -> list[SplitOdometry]:
    """Splits odometry-based parent measurements into 2 children measurements with the
    same value but different timestamps.

    Args:
        measurements: parent measurements to split.

    Returns:
        list of children measurements.
    """
    new_measurements = []
    for m in measurements:
        m1, m2 = split_one(m)
        new_measurements.append(m1)
        new_measurements.append(m2)
    return new_measurements
