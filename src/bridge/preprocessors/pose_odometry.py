from collections.abc import Iterable

from src.measurement_storage.measurements.auxiliary import SplitPoseOdometry
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.pose_odometry import Odometry


def split_odometry(measurements: Iterable[Measurement], start: int | None) -> list[Measurement]:
    """Finds and replaces odometry measurements in the sequence of measurements.

    Args:
        measurements: a sequence of measurements.

        start: a start time limit.

    Returns:
        split measurements.

    TODO: add tests.
    """
    splits = split(measurements, start)
    parents = set(m.parent for m in splits)
    new_measurements = [m for m in measurements if m not in parents]
    new_measurements.extend(splits)
    return new_measurements


def split(measurements: Iterable[Measurement], start: int | None) -> list[SplitPoseOdometry]:
    """Splits PoseOdometry measurements (inside time_range only) into children measurements with the same
    parent but different timestamps.

    Args:
        measurements: parent measurements to split.

        start: start time limit.

    Returns:
        split pose odometries.
    """
    splits = []

    for m in measurements:
        if isinstance(m, Odometry):
            m_start = m.time_range.start
            m_stop = m.time_range.stop

            if start is None:
                m1 = SplitPoseOdometry(m_start, m)
                m2 = SplitPoseOdometry(m_stop, m)
                splits.append(m1)
                splits.append(m2)

            else:
                if start < m_start:
                    m1 = SplitPoseOdometry(m_start, m)
                    m2 = SplitPoseOdometry(m_stop, m)
                    splits.append(m1)
                    splits.append(m2)

    return splits
