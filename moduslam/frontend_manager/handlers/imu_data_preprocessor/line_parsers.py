"""Methods to parse IMU data from different datasets.

First value in the line is the timestamp and is not included in the values.
"""

from dataclasses import dataclass


@dataclass
class ImuData:
    angular_velocity: tuple[float, float, float]
    acceleration: tuple[float, float, float]


def get_kaist_imu_data(values: tuple[float, ...]) -> ImuData:
    """Extracts IMU data from a line of KAIST dataset.

    Args:
        values: line with imu data.

    Returns:
        ImuData instance.
    """
    angular_velocity = values[7], values[8], values[9]
    acceleration = values[10], values[11], values[12]
    return ImuData(angular_velocity, acceleration)


def get_tum_vie_imu_data(values: tuple[float, ...]) -> ImuData:
    """Extracts IMU data from a line of TUM VIE dataset.

    Args:
        values: line with imu data.

    Returns:
        ImuData instance.
    """
    angular_velocity = values[0], values[1], values[2]
    acceleration = values[3], values[4], values[5]
    return ImuData(angular_velocity, acceleration)
