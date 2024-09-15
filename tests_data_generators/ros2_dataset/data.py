"""Ros2 dataset-like data."""

from pathlib import Path

import pandas as pd

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensors import SensorConfig

# TODO: Create a class to get the ground truth elements from a test rosbag instead of using a CSV file
data = pd.read_csv(
    Path("/home/felipezero/Projects/mySLAM/tests_data/ROS2_dataset/rosbags_raw_data.csv")
)

sensors_table = {
    "stereo_camera_left": "left",
    "stereo_camera_right": "right",
    "imu": "imu",
    "lidar_left": "vlp16l",
    "lidar_right": "vlp16r",
    "lidar_center": "vlp32c",
}

sensors = {
    "imu": Sensor(SensorConfig(sensors_table["imu"])),
    "stereo_camera_left": Sensor(SensorConfig(sensors_table["stereo_camera_left"])),
    "stereo_camera_right": Sensor(SensorConfig(sensors_table["stereo_camera_right"])),
    "lidar_left": Sensor(SensorConfig(sensors_table["lidar_left"])),
    "lidar_right": Sensor(SensorConfig(sensors_table["lidar_right"])),
    "lidar_center": Sensor(SensorConfig(sensors_table["lidar_center"])),
}


elements = []

for index, sensor_reading in data.iterrows():
    timestamp = sensor_reading.timestamp
    raw_values = sensor_reading.data
    sensor = sensors[sensor_reading.sensor_name]

    raw_measurement = RawMeasurement(sensor=sensor, values=raw_values)
    element = Element(timestamp=timestamp, measurement=raw_measurement, location=index)

    elements.append(element)
