"""Ros2 dataset-like data."""
from pathlib import Path
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from moduslam.data_manager.batch_factory.readers.ros2.utils import read_rosbag
from tests.conftest import ros2_dataset_dir

# Указываем путь к rosbag
rosbag_path = Path(ros2_dataset_dir)

sensors_table = {
    "left": "/left/image_raw",
    "right": "/right/image_raw",
    "xsens": "/xsens/imu/data",
    "vlp16l": "/vlp16l/velodyne_points",
    "vlp16r": "/vlp16r/velodyne_points",
    "vlp32c": "/vlp32c/velodyne_points",
}

elements_iterator = read_rosbag(bag_path=rosbag_path, topics_table=sensors_table, mode="stream")
elements = list(read_rosbag(bag_path=rosbag_path, topics_table=sensors_table, mode="stream"))





