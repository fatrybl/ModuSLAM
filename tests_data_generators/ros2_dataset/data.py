"""Ros2 dataset-like data."""

from pathlib import Path

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.locations import RosbagLocation
from moduslam.data_manager.batch_factory.readers.ros2.measurement_collector import (
    get_imu_measurement,
    get_lidar_measurement,
    get_stereo_measurement,
)
from moduslam.data_manager.batch_factory.readers.ros2.utils import rosbag_read
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from tests.conftest import ros2_dataset_dir

# TODO: Create a class to get the ground truth elements from a test rosbag instead of using a CSV file


rosbag_path = Path(ros2_dataset_dir)

data = rosbag_read(bag_path=rosbag_path, num_readings=100)

sensors_table = {
    "left": "stereo_camera_left",
    "right": "stereo_camera_right",
    "xsens": "imu",
    "vlp16l": "lidar_left",
    "vlp16r": "lidar_right",
    "vlp32c": "lidar_center",
}

data_getters = {
    "data": get_imu_measurement,
    "velodyne_points": get_lidar_measurement,
    "image_raw": get_stereo_measurement,
}


elements = []

for i, row in enumerate(data):
    topic = row[1]
    sensor_topic = topic.split("/")[1]
    data_type = topic.split("/")[-1]

    if sensor_topic in sensors_table.keys() and data_type in data_getters.keys():
        sensor_name = sensors_table[sensor_topic]

        raw_data = row[6]
        timestamp = row[5]
        message_getter = data_getters[data_type]
        sensor_data = message_getter(raw_data)

        sensor = Sensor(SensorConfig(sensor_name))

        measurement = RawMeasurement(sensor=sensor, values=sensor_data)

        location = RosbagLocation(file=rosbag_path, position=i)

        element = Element(
            timestamp=timestamp,
            measurement=measurement,
            location=location,
        )

        elements.append(element)
