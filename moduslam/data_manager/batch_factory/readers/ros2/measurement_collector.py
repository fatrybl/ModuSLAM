import numpy as np


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


def image_decoding(raw_image_msg) -> TupleImage:
    """Decodes a ROS2 Image message into an array.

    Args:
        raw_image_msg: a ROS2 Image message.

    Returns:
        image_tuple: a tuple with the image data.

    Raises:
        ValueError: if the encoding is not supported.
    """
    # TODO: Either add more functions with different encodings. Be more SPECIFIC with function names

    height = raw_image_msg.height
    width = raw_image_msg.width
    steps = raw_image_msg.step
    encoding = raw_image_msg.encoding
    bgr_num_channels = 3

    print(height, width, steps, encoding)

    if encoding == "bgr8":
        np_array = np.frombuffer(raw_image_msg.data, np.uint8).reshape(
            (height, width, bgr_num_channels)
        )
        image_list = np_array.tolist()

        # TODO: Transform np array into a TupleImage format.

        return image_tuple
    else:
        raise ValueError("Encoding {} is not supported".format(encoding))


def convert2image(img_array, encoding: str):
    """Converts an array into a PIL image.
    Args:
        img_array: an array to be converted to a PIL Image.
        encoding: the encoding of the image.

     Returns:
        pil_img: a PIL Image object.
    """

    if isinstance(img_array, np.ndarray):
        print("Converting numpy array to PIL Image")
        if encoding == "bgr8":
            pil_img = Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))

    elif isinstance(img_array, (list, tuple)):
        print("Converting list to PIL Image")
        img_array = np.array(img_array)
        if encoding == "bgr8":
            pil_img = Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))

    else:
        raise ValueError("Array type {} is not supported".format(type(img_array)))
