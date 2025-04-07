from collections.abc import Callable

from src.moduslam.data_manager.batch_factory.data_readers.ros2.msg_processors.s3e_dataset.processors import (
    get_2d_pointcloud,
    get_3d_pointcloud,
    get_image,
    get_imu_measurement,
)

table: dict[str, Callable] = {
    "sensor_msgs/msg/Imu": get_imu_measurement,
    "sensor_msgs/msg/LaserScan": get_2d_pointcloud,
    "sensor_msgs/msg/PointCloud": get_3d_pointcloud,
    "sensor_msgs/msg/PointCloud2": get_3d_pointcloud,
    "sensor_msgs/msg/Image": get_image,
    "sensor_msgs/msg/CompressedImage": get_image,
}
