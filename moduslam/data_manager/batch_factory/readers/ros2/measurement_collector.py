from typing import TypeAlias

import numpy as np

TupleImage: TypeAlias = tuple[list[list[int]]]


def get_stereo_measurement(raw_msg) -> TupleImage:
    """Transform raw stereo image messages from a rosbag into an image-like array.
    Args:
        raw_msg: raw stereo image message.

    Returns:
        img_array: image-like array.
    """

    encoding = raw_msg.encoding

    if encoding == "bgr8":
        img_array = image_decoding_bgr8(raw_image_msg=raw_msg)

        return img_array

    else:
        raise ValueError("Encoding {} is not supported".format(encoding))


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
    data = tuple(raw_msg.data)

    return data

def get_gps_measurement(raw_msg) -> tuple:
    """Transform raw GPS messages from a rosbag into a tuple.

    Args:
        raw_msg: raw GPS message.

    Returns:
        data: tuple with the GPS data.
    """
    latitude = raw_msg.latitude
    longitude = raw_msg.longitude
    altitude = raw_msg.altitude

    gps_data = (latitude, longitude, altitude)
    return gps_data

def get_odometry_measurement(raw_msg) -> tuple:
    """Transform raw Odometry messages from a rosbag into a tuple.

    Args:
        raw_msg: raw Odometry message.

    Returns:
        data: tuple with the Odometry data.
    """
    position = raw_msg.pose.pose.position
    orientation = raw_msg.pose.pose.orientation
    linear_velocity = raw_msg.twist.twist.linear
    angular_velocity = raw_msg.twist.twist.angular

    odometry_data = (
        position.x, position.y, position.z,
        orientation.x, orientation.y, orientation.z, orientation.w,
        linear_velocity.x, linear_velocity.y, linear_velocity.z,
        angular_velocity.x, angular_velocity.y, angular_velocity.z
    )
    return odometry_data

def image_decoding_bgr8(raw_image_msg) -> TupleImage:
    """Decodes a ROS2 Image message into an array.

    Args:
        raw_image_msg: a ROS2 Image message.

    Returns:
        image_tuple: a tuple with the image data.

    Raises:
        ValueError: if the encoding is not supported.
    """
    height = raw_image_msg.height
    width = raw_image_msg.width
    bgr_num_channels = 3

    np_array = np.frombuffer(raw_image_msg.data, np.uint8).reshape(
        (height, width, bgr_num_channels)
    )
    image_tuple = tuple(np_array.tolist())

    return image_tuple


def convert2image(img_tuple: TupleImage, encoding: str):
    """Converts an array into a PIL image.
    Args:
        img_array: an array to be converted to a PIL Image.
        encoding: the encoding of the image.

     Returns:
        pil_img: a PIL Image object.
    """

    import cv2

    img = np.array(img_tuple, dtype=np.uint8)
    print("Image shape: ", img.shape)
    if encoding == "bgr8":
        cv2.imshow("test", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        raise ValueError("Encoding {} is not supported".format(encoding))
