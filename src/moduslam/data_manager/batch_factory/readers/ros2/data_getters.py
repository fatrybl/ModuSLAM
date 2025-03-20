from collections.abc import Callable
from moduslam.data_manager.batch_factory.readers.ros2.measurement_collector import (
    get_imu_measurement,
    get_lidar_measurement,
    get_stereo_measurement,
    get_gps_measurement,
    get_odometry_measurement,
    get_laser_scan_measurement,
)

data_getter: dict[str, Callable] = {
    "Imu": get_imu_measurement,
    "PointCloud2": get_lidar_measurement,
    "Image": get_stereo_measurement,
    "GPS": get_gps_measurement,
    # "Odometry": get_odometry_measurement,
    "LaserScan": get_laser_scan_measurement,
}