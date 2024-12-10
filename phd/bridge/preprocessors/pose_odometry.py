from collections.abc import Iterable

from phd.measurement_storage.measurements.auxiliary import SplitPoseOdometry
from phd.measurement_storage.measurements.base import Measurement
from phd.measurement_storage.measurements.pose_odometry import Odometry


def remove_odometry(measurements: list[Measurement]) -> list[Measurement]:
    """Removes odometry measurements from the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        measurements without odometry measurements.
    """
    return [m for m in measurements if not isinstance(m, Odometry)]


def find_and_replace(measurements: Iterable[Measurement]) -> list[Measurement]:
    """Finds and replaces odometry measurements in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        split measurements.
    """
    splits = split(measurements)
    parents = set(m.parent for m in splits)
    new_measurements = [m for m in measurements if m not in parents]
    new_measurements.extend(splits)
    return new_measurements


def split(measurements: Iterable[Measurement]) -> list[SplitPoseOdometry]:
    """Splits PoseOdometry measurements into 2 children measurements with the same
    parent but different timestamps.

    Args:
        measurements: parent measurements to split.

    Returns:
        split pose odometries.
    """
    splits = []

    for m in measurements:
        if isinstance(m, Odometry):
            m1 = SplitPoseOdometry(m.time_range.start, m)
            m2 = SplitPoseOdometry(m.time_range.stop, m)
            splits.append(m1)
            splits.append(m2)

    return splits
