from collections.abc import Iterable

from phd.external.objects.measurements import Measurement, SplitPoseOdometry
from phd.measurements.processed_measurements import PoseOdometry


def remove_odometry(measurements: list[Measurement]) -> list[Measurement]:
    """Removes odometry measurements from the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        measurements without odometry measurements.
    """
    return [m for m in measurements if not isinstance(m, PoseOdometry)]


def find_and_split(measurements: Iterable[Measurement]) -> list[SplitPoseOdometry] | None:
    """Finds and splits odometry measurements in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        odometry measurements if found or None.

    TODO: check if any odometry.time_range.start is inside the time range of all measurements.
        if not: do not split.
    """
    odometry_measurements = get_odometry_measurements(measurements)
    if odometry_measurements:
        splits = split_multiple(odometry_measurements)
        return splits
    else:
        return None


def get_odometry_measurements(measurements: Iterable[Measurement]) -> list[PoseOdometry]:
    """Finds all odometry measurements in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        odometry measurements.
    """
    odometry_measurements = [m for m in measurements if isinstance(m, PoseOdometry)]
    return odometry_measurements


def split_one(measurement: PoseOdometry) -> tuple[SplitPoseOdometry, SplitPoseOdometry]:
    """Splits odometry-based parent measurement into 2 children measurements with the
    same value but different timestamps.

    Args:
        measurement: parent measurement to split.

    Returns:
        2 children measurements.
    """
    m1 = SplitPoseOdometry(measurement.time_range.start, measurement)
    m2 = SplitPoseOdometry(measurement.time_range.stop, measurement)
    return m1, m2


def split_multiple(measurements: Iterable[PoseOdometry]) -> list[SplitPoseOdometry]:
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
