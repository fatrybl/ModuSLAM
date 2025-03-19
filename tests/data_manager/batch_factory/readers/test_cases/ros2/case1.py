from pathlib import Path
from moduslam.data_manager.batch_factory.readers.ros2.reader import Ros2DataReader
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import Ros2Config
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from tests.conftest import ros2_dataset_dir
from tests_data_generators.ros2_dataset.data import elements
from tests_data_generators.utils import generate_sensors_factory_config
from moduslam.data_manager.batch_factory.readers.ros2.utils import read_rosbag

# Путь к Rosbag
rosbag_path = Path(ros2_dataset_dir)

print(f"Debug: Checking rosbag path - {rosbag_path}")
print("Debug: Path exists?", rosbag_path.exists())


# Таблица топиков
sensors_table = {
    "left": "/left/image_raw",
    "right": "/right/image_raw",
    "xsens": "/xsens/imu/data",
    "vlp16l": "/vlp16l/velodyne_points",
    "vlp16r": "/vlp16r/velodyne_points",
    "vlp32c": "/vlp32c/velodyne_points",
}

# Читаем данные из Rosbag (итератор)
elements_iterator = read_rosbag(bag_path=rosbag_path, topics_table=sensors_table, mode="stream")

# Проверяем, есть ли данные
try:
    first_element = next(elements_iterator)  # Берём первый элемент
    elements = [first_element] + list(elements_iterator)  # Создаём список
except StopIteration:
    raise ValueError("Error: elements list is empty! Check read_rosbag function or rosbag path.")

print("Debug: Successfully loaded", len(elements), "elements")

# Извлекаем первые 5 элементов
el1, el2, el3, el4, el5 = (next(iter(elements)) for _ in range(5))

# Временные метки
timestamp1 = 1698927496694033807
timestamp2 = 1698927496739239954  # 20 sensor readings
timestamp3 = 1698927496799306816  # 40 sensor readings
timestamp4 = 1698927496898641344  # 60 sensor readings
timestamp5 = 1698927497046583719  # 80 sensor readings
timestamp6 = 1698927497190095250  # 100 sensor readings

# Фильтруем элементы по временным меткам
elements_0_20 = [e for e in elements if timestamp1<= e[0] < timestamp2]
elements20_40 = [e for e in elements if timestamp2 <= e[0] < timestamp3]
elements40_60 = [e for e in elements if timestamp3 <= e[0] < timestamp4]
elements60_80 = [e for e in elements if timestamp4 <= e[0] < timestamp5]
elements80_100 = [e for e in elements if timestamp5 <= e[0] < timestamp6]


# Конфигурация сенсоров
sensors_table1 = {
    "stereo_camera_left": "left",
    "stereo_camera_right": "right",
    "imu": "xsens",
    "lidar_left": "vlp16l",
    "lidar_right": "vlp16r",
    "lidar_center": "vlp32c",
}
sensors1 = [Sensor(SensorConfig(sensor_name)) for sensor_name in sensors_table1.keys()]

dataset_cfg1 = Ros2Config(directory=ros2_dataset_dir, sensors_table=sensors_table1, topics_table=sensors_table)
stream = Stream()

# Конфигурация фабрики сенсоров
sensors_factory_config1 = generate_sensors_factory_config(sensors1)

# Временные режимы
timelimit20 = TimeLimit(start=timestamp1, stop=timestamp2)
timelimit20_40 = TimeLimit(start=timestamp2, stop=timestamp3)
timelimit40_60 = TimeLimit(start=timestamp3, stop=timestamp4)
timelimit60_80 = TimeLimit(start=timestamp4, stop=timestamp5)
timelimit80_100 = TimeLimit(start=timestamp5, stop=timestamp6)

# Тестовые сценарии
# valid_stream_scenarios = (
#     (sensors_factory_config1, dataset_cfg1, stream, Ros2DataReader, elements),
# )

valid_timelimit_scenarios = (
    (sensors_factory_config1, dataset_cfg1, timelimit20, Ros2DataReader, elements_0_20),
    (sensors_factory_config1, dataset_cfg1, timelimit20_40, Ros2DataReader, elements20_40),
    (sensors_factory_config1, dataset_cfg1, timelimit40_60, Ros2DataReader, elements40_60),
    (sensors_factory_config1, dataset_cfg1, timelimit80_100, Ros2DataReader, elements80_100),
)

# stream_scenarios = (
#     *valid_stream_scenarios,
# )

time_limit_scenarios = (
    *valid_timelimit_scenarios,
)

ros2_case1 = (

    *time_limit_scenarios,
)
