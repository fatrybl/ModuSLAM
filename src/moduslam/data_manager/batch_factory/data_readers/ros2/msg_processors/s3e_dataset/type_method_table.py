from collections.abc import Callable

from src.moduslam.data_manager.batch_factory.data_readers.ros2.msg_processors.s3e_dataset.processors import (
    get_3d_pointcloud,
    get_image,
    get_imu_measurement,
    get_navsat_fix,
    get_quaternion_stamped,
    get_time_reference,
    get_twist_stamped,
    get_uwb,
)

table: dict[str, Callable] = {
    "sensor_msgs/msg/Imu": get_imu_measurement,
    "sensor_msgs/msg/PointCloud2": get_3d_pointcloud,
    "sensor_msgs/msg/CompressedImage": get_image,
    "sensor_msgs/msg/NavSatFix": get_navsat_fix,
    "std_msgs/msg/Float64MultiArray": get_uwb,
    "sensor_msgs/msg/TimeReference": get_time_reference,
    "geometry_msgs/msg/TwistStamped": get_twist_stamped,
    "geometry_msgs/msg/QuaternionStamped": get_quaternion_stamped,
}
