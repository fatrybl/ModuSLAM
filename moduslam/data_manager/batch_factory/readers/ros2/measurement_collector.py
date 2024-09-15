import numpy as np

from moduslam.data_manager.batch_factory.readers.ros2.utils import (
    image_decoding,
    convert2image,
)


def get_stereo_measurement(raw_msg) -> tuple:
    """Transform raw stereo image messages from a rosbag into an image-like array.
    Args:
        raw_msg: raw stereo image message.

    Returns:
        img_array: image-like array.
    """

    print(type(raw_msg))
    encoding = raw_msg.encoding

    img_array = image_decoding(raw_image_msg=raw_msg)

    # Convert the array into a PIL Image
    img = convert2image(img_array, encoding)

    # pil_img.show()

    return img_array


def get_imu_measurement(raw_msg) -> tuple:
    """Transform raw IMU messages from a rosbag into a tuple.
    Args:
        raw_msg: raw IMU message.

    Returns:
        imu_data: tuple with the IMU data.

    """
    orientation = raw_msg.orientation
    angular_velocity = raw_msg.angular_velocity
    linear_acceleration = raw_msg.linear_acceleration
    orientation_x = orientation.x
    orientation_y = orientation.y
    orientation_z = orientation.z
    orientation_w = orientation.w
    angular_velocity_x = angular_velocity.x
    angular_velocity_y = angular_velocity.y
    angular_velocity_z = angular_velocity.z
    linear_acceleration_x = linear_acceleration.x
    linear_acceleration_y = linear_acceleration.y
    linear_acceleration_z = linear_acceleration.z

    imu_data = (
        orientation_x,
        orientation_y,
        orientation_z,
        orientation_w,
        angular_velocity_x,
        angular_velocity_y,
        angular_velocity_z,
        linear_acceleration_x,
        linear_acceleration_y,
        linear_acceleration_z,
    )
    return imu_data


def get_lidar_measurement(raw_msg) -> tuple:
    """Transform raw LiDAR messages from a rosbag into a tuple.
    Args:
        raw_msg: raw LiDAR message.

    Returns:
        data: tuple with the LiDAR data.

    """
    data = np.array(raw_msg.data)

    data = tuple(raw_msg.data)

    return data
