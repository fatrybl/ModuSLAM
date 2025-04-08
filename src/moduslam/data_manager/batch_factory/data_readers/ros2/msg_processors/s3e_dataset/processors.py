from io import BytesIO
from typing import TypeAlias

from PIL import Image as ImageIO
from PIL.Image import Image

from src.custom_types.aliases import Vector6
from src.custom_types.numpy import MatrixMxN
from src.moduslam.data_manager.batch_factory.data_readers.ros2.utils.point_cloud2_processor import (
    filter_nans,
    pointcloud2_to_array,
    structured_to_regular_array,
)
from src.utils.exceptions import ExternalModuleException

StereoImage: TypeAlias = tuple[Image, Image]


def get_image(raw_msg) -> Image:
    """Gets an image with PIL library.
    Args:
        raw_msg: raw message.

    Returns:
        image.
    """
    buffer = BytesIO(raw_msg.data)
    try:
        img = ImageIO.open(buffer)

    except Exception as e:
        raise ExternalModuleException(e)

    return img


def get_navsat_fix(raw_msg) -> Vector6:
    """Gets raw NavSatFix message.

    Args:
        raw_msg: raw NavSatFix message.

    Returns:
        NavSatFix data: latitude, longitude, altitude, covariance, covariance_type, status.
    """
    latitude = raw_msg.latitude
    longitude = raw_msg.longitude
    altitude = raw_msg.altitude
    covariance = raw_msg.position_covariance
    covariance_type = raw_msg.position_covariance_type
    status = raw_msg.status

    return latitude, longitude, altitude, covariance, covariance_type, status


def get_imu_measurement(raw_msg) -> Vector6:
    """Gets linear acceleration & angular velocity data.
    Args:
        raw_msg: raw IMU message.

    Returns:
        imu_data: a_x, a_y, a_z, w_x, w_y, w_z.

    """
    linear_acceleration = raw_msg.linear_acceleration
    angular_velocity = raw_msg.angular_velocity

    a_x = linear_acceleration.x
    a_y = linear_acceleration.y
    a_z = linear_acceleration.z
    w_x = angular_velocity.x
    w_y = angular_velocity.y
    w_z = angular_velocity.z

    return a_x, a_y, a_z, w_x, w_y, w_z


def get_2d_pointcloud(raw_msg) -> tuple:
    """Transform raw LaserScan messages from a rosbag into a tuple.

    Args:
        raw_msg: raw LaserScan message.

    Returns:
        data: tuple with the LaserScan data.
    """
    ranges = tuple(raw_msg.ranges)
    intensities = tuple(raw_msg.intensities)

    laser_scan_data = (ranges, intensities)
    return laser_scan_data


def get_3d_pointcloud(raw_msg) -> MatrixMxN:
    """Processes raw LiDAR ROS-2 PointCloud2 message into a NumPy array [NxM].

    Args:
        raw_msg: a PointCloud2 message.

    Returns:
        points array.
    """
    structured = pointcloud2_to_array(raw_msg)
    points = structured_to_regular_array(structured)
    points = filter_nans(points)

    return points


def get_uwb(raw_msg) -> tuple:
    """Gets raw Ultra Wide Band message.

    Args:
        raw_msg: raw UWB message.

    Returns:
        data: tuple with the UWB data.
    """
    raise NotImplementedError


def get_time_reference(raw_msg) -> tuple:
    """Gets raw TimeReference message.

    Args:
        raw_msg: raw TimeReference message.

    Returns:
        data: tuple with the TimeReference data.
    """
    raise NotImplementedError


def get_twist_stamped(raw_msg) -> tuple:
    """Gets raw TwistStamped message.

    Args:
        raw_msg: raw TwistStamped message.

    Returns:
        data: tuple with the TwistStamped data.
    """
    raise NotImplementedError


def get_quaternion_stamped(raw_msg) -> tuple:
    """Gets raw QuaternionStamped message.

    Args:
        raw_msg: raw QuaternionStamped message.

    Returns:
        data: tuple with the QuaternionStamped data.
    """
    raise NotImplementedError
