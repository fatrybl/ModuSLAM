# """Ros2 dataset-like data."""
#
# from pathlib import Path
#
# from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
# from moduslam.data_manager.batch_factory.readers.locations import RosbagLocation
# from moduslam.data_manager.batch_factory.readers.ros2.measurement_collector import (
#     get_imu_measurement,
#     get_lidar_measurement,
#     get_stereo_measurement,
# )
# from moduslam.data_manager.batch_factory.readers.ros2.utils import rosbag_read
# from moduslam.setup_manager.sensors_factory.sensors import Sensor
# from moduslam.system_configs.setup_manager.sensors import SensorConfig
# from tests.conftest import ros2_dataset_dir
#
# rosbag_path = Path(ros2_dataset_dir)
#
# data = rosbag_read(bag_path=rosbag_path, num_readings=100)
#
# sensors_table = {
#     "left": "stereo_camera_left",
#     "right": "stereo_camera_right",
#     "xsens": "imu",
#     "vlp16l": "lidar_left",
#     "vlp16r": "lidar_right",
#     "vlp32c": "lidar_center",
# }
#
# data_getters = {
#     "data": get_imu_measurement,
#     "velodyne_points": get_lidar_measurement,
#     "image_raw": get_stereo_measurement,
# }
#
#
# elements = []
#
# for i, row in enumerate(data):
#     topic = row[1]
#     sensor_topic = topic.split("/")[1]
#     data_type = topic.split("/")[-1]
#
#     if sensor_topic in sensors_table.keys() and data_type in data_getters.keys():
#         sensor_name = sensors_table[sensor_topic]
#
#         raw_data = row[6]
#         timestamp = row[5]
#         message_getter = data_getters[data_type]
#         sensor_data = message_getter(raw_data)
#
#         sensor = Sensor(SensorConfig(sensor_name))
#
#         measurement = RawMeasurement(sensor=sensor, values=sensor_data)
#
#         location = RosbagLocation(file=rosbag_path, position=i)
#
#         element = Element(
#             timestamp=timestamp,
#             measurement=measurement,
#             location=location,
#         )
#
#         elements.append(element)
"""Ros2 dataset-like data."""
from pathlib import Path
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from moduslam.data_manager.batch_factory.readers.ros2.utils import read_rosbag
from tests.conftest import ros2_dataset_dir

# Указываем путь к rosbag
rosbag_path = Path(ros2_dataset_dir)

# Таблица топиков, аналогично ридеру
sensors_table = {
    "left": "/left/image_raw",
    "right": "/right/image_raw",
    "xsens": "/xsens/imu/data",
    "vlp16l": "/vlp16l/velodyne_points",
    "vlp16r": "/vlp16r/velodyne_points",
    "vlp32c": "/vlp32c/velodyne_points",
}

# Загружаем данные
elements_iterator = read_rosbag(bag_path=rosbag_path, topics_table=sensors_table, mode="stream")

# Создаем список элементов
elements_list = [elem for elem in elements_iterator]  # Создаем список сразу

print("Debug: Преобразование итератора в список прошло успешно.")
print("Debug: Длина elements:", len(elements_list))

if not elements_list:
    raise ValueError("Error: elements list is empty! Check read_rosbag function or rosbag path.")



