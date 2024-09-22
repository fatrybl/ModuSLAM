"""Ros2 dataset-like data."""

from pathlib import Path

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.locations import RosbagLocation
from moduslam.data_manager.batch_factory.readers.ros2.measurement_collector import (
    get_imu_measurement,
    get_stereo_measurement,
    get_lidar_measurement,
)
from moduslam.data_manager.batch_factory.readers.ros2.utils import rosbag_read
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensors import SensorConfig

# TODO: Create a class to get the ground truth elements from a test rosbag instead of using a CSV file

DATA_PATH = "/home/felipezero/Projects/mySLAM_data/20231102_kia/"
test_bag = "test_rosbag_100"

rosbag_path = Path(DATA_PATH, test_bag)

data = rosbag_read(bag_path=rosbag_path, num_readings=100, print_table=False)

sensors_table = {
    "left": "stereo_camera_left",
    "right": "stereo_camera_right",
    "xsens": "imu",
    "vlp16l": "lidar_left",
    "vlp16r": "lidar_right",
    "vlp32c": "lidar_ceter",
}

test_dict = {
    "data": get_imu_measurement,
    "velodyne_points": get_lidar_measurement,
    "image_raw": get_stereo_measurement,
}


elements = []
count = 0
for i, row in enumerate(data):
    topic = row[1]
    sensor_topic = topic.split("/")[1]
    data_type = topic.split("/")[-1]

    if sensor_topic in sensors_table.keys() and data_type in test_dict.keys():
        sensor_name = sensors_table[sensor_topic]

        raw_data = row[6]
        timestamp = row[5]
        message_getter = test_dict[data_type]
        data = message_getter(raw_data)

        sensor = Sensor(SensorConfig(sensor_name))

        measurement = RawMeasurement(sensor=sensor, values=data)

        location = RosbagLocation(file=rosbag_path, position=i - 1)

        element = Element(
            timestamp=timestamp,
            measurement=measurement,
            location=location,
        )

        elements.append(element)
        count += 1

print(len(elements))

element = elements[0]

print(element.timestamp)
print(element.measurement.values)
