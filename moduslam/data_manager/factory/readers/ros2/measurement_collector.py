from rosbags.serde import deserialize_cdr


class RawDataCollector:
    def __init__(self, topic_name, msg_type):
        self.topic_name = topic_name
        self.msg_type = msg_type
        self.data = []

    def get_imu_data(self, msg: bytes, message_type: str):
        # TODO: ADD docstrings to every function
        msg = deserialize_cdr(msg, message_type)
        orientation = msg.orientation
        angular_velocity = msg.angular_velocity
        linear_acceleration = msg.linear_acceleration

    def get_camera_data(self, msg, message_type):
        msg = deserialize_cdr(msg, message_type)
        image = msg.image
        return image

    def get_lidar_data(self, msg, message_type):
        msg = deserialize_cdr(msg, message_type)
        scan = msg.scan
        return scan
