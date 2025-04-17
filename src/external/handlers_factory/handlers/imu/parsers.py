"""Parsers of IMU data collected with different Data Readers from different datasets."""

from collections.abc import Callable

from src.custom_types.aliases import Vector6
from src.measurement_storage.measurements.imu import ImuData
from src.moduslam.data_manager.batch_factory.configs import DataReaders
from src.utils.auxiliary_methods import str_to_float


def parse_kaist_urban(values: tuple[str, ...]) -> ImuData:
    """Extracts IMU data from a line of Kaist Urban dataset.

    IMU data format: [
            quaternion x, quaternion y, quaternion z, quaternion w,
            Euler x, Euler y, Euler z,
            Gyro x, Gyro y, Gyro z,
            Acceleration x, Acceleration y, Acceleration z,
            MagnetField x, MagnetField y, MagnetField z
            ]

    timestamp is not present in values.

    Args:
        values: tuple of values as strings.

    Returns:
        IMU data.
    """
    wx = str_to_float(values[7])
    wy = str_to_float(values[8])
    wz = str_to_float(values[9])
    ax = str_to_float(values[10])
    ay = str_to_float(values[11])
    az = str_to_float(values[12])
    return ImuData((wx, wy, wz), (ax, ay, az))


def parse_tum_vie(values: tuple[str, ...]) -> ImuData:
    """Extracts IMU data from a line of TUM Vie dataset.

    Args:
        values: tuple of values as strings.

    IMU data format: [
        gx(rad/s), gy(rad/s), gz(rad/s),
        ax(m/s^2), ay(m/s^2), az(m/s^2),
        exposure time
    ]

    timestamp is not present in values.

    Returns:
        IMU data.
    """
    wx = str_to_float(values[0])
    wy = str_to_float(values[1])
    wz = str_to_float(values[2])
    ax = str_to_float(values[3])
    ay = str_to_float(values[4])
    az = str_to_float(values[5])
    return ImuData((wx, wy, wz), (ax, ay, az))


def parse_ros_message(values: Vector6) -> ImuData:
    """Extracts IMU data from a ROS message.

    Args:
        values: vector with 6 floats.

    IMU data format: [
        Gyro x, Gyro y, Gyro z,
        Acceleration x, Acceleration y, Acceleration z
    ]

    timestamp is not present in values.

    Returns:
        IMU data.
    """
    w_x, w_y, w_z = values[0], values[1], values[2]
    a_x, a_y, a_z = values[3], values[4], values[5]

    return ImuData((w_x, w_y, w_z), (a_x, a_y, a_z))


dataset_parser_mapping: dict[str, Callable[[tuple], ImuData]] = {
    DataReaders.kaist_urban: parse_kaist_urban,
    DataReaders.tum_vie: parse_tum_vie,
    DataReaders.ros2: parse_ros_message,
}
