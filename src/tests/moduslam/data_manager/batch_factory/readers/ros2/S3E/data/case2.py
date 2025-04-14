from src.moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2HumbleConfig,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.sensors import Sensor
from src.tests.conftest import s3e_dataset_dir
from src.tests_data_generators.ros2.s3e_dataset.data import (
    Data,
    imu,
    imu_cfg,
    left_camera,
    left_camera_cfg,
    lidar,
    lidar_cfg,
    right_camera_cfg,
    rtk_cfg,
    sensor_name_topic_map,
)

data = Data(s3e_dataset_dir)
elements = data.elements

imu_elements = [el for el in elements if el.measurement.sensor.name == imu_cfg.name]
lidar_elements = [el for el in elements if el.measurement.sensor.name == lidar_cfg.name]
left_camera_elements = [el for el in elements if el.measurement.sensor.name == left_camera_cfg.name]

left_camera_lidar_elements = sorted(
    lidar_elements + left_camera_elements, key=lambda el: el.timestamp
)

all_sensors: list[Sensor] = [element.measurement.sensor for element in elements]

dataset_cfg = Ros2HumbleConfig(
    directory=s3e_dataset_dir, sensor_topic_mapping=sensor_name_topic_map
)

stream = Stream()
t_limit_0 = TimeLimit(elements[0].timestamp, elements[-1].timestamp)
t_limit_1 = TimeLimit(elements[0].timestamp, elements[0].timestamp)
t_limit_2 = TimeLimit(elements[-1].timestamp, elements[-1].timestamp)
t_limit_3 = TimeLimit(imu_elements[0].timestamp, imu_elements[-1].timestamp)
t_limit_4 = TimeLimit(lidar_elements[0].timestamp, lidar_elements[-1].timestamp)
t_limit_5 = TimeLimit(
    left_camera_lidar_elements[0].timestamp, left_camera_lidar_elements[-1].timestamp
)
t_limit_6 = TimeLimit(left_camera_elements[0].timestamp, left_camera_elements[1].timestamp)

sensors_configs_1 = [imu_cfg, lidar_cfg, left_camera_cfg, right_camera_cfg, rtk_cfg]
sensors_configs_2 = [imu_cfg]
sensors_configs_3 = [left_camera_cfg, lidar_cfg]

imu_list = [imu] * len(imu_elements)
lidar_list = [lidar] * len(lidar_elements)
left_camera_list = [left_camera] * len(left_camera_elements)
left_camera_lidar_sensors = [el.measurement.sensor for el in left_camera_lidar_elements]

valid_stream_scenarios = (
    (sensors_configs_1, dataset_cfg, stream, all_sensors, elements),
    (sensors_configs_1, dataset_cfg, stream, imu_list, imu_elements),
    (sensors_configs_1, dataset_cfg, stream, lidar_list, lidar_elements),
    (sensors_configs_1, dataset_cfg, stream, left_camera_lidar_sensors, left_camera_lidar_elements),
    (sensors_configs_2, dataset_cfg, stream, imu_list, imu_elements),
    (sensors_configs_3, dataset_cfg, stream, left_camera_lidar_sensors, left_camera_lidar_elements),
    (sensors_configs_1, dataset_cfg, stream, all_sensors, [*elements, None]),
)

valid_timelimit_scenarios = (
    (sensors_configs_1, dataset_cfg, t_limit_0, all_sensors, elements),
    (sensors_configs_2, dataset_cfg, t_limit_0, imu_list, imu_elements),
    (sensors_configs_2, dataset_cfg, t_limit_3, imu_list, imu_elements),
    (sensors_configs_3, dataset_cfg, t_limit_4, lidar_list, lidar_elements),
    (
        sensors_configs_3,
        dataset_cfg,
        t_limit_5,
        left_camera_lidar_sensors,
        left_camera_lidar_elements,
    ),
    (sensors_configs_3, dataset_cfg, t_limit_6, left_camera_list[:2], left_camera_elements[:2]),
    (sensors_configs_1, dataset_cfg, t_limit_1, [left_camera, left_camera], [None, None]),
    (sensors_configs_1, dataset_cfg, t_limit_2, [imu, lidar], [imu_elements[-1], None]),
    (sensors_configs_1, dataset_cfg, t_limit_1, [lidar, lidar], [lidar_elements[0], None]),
)

S3E_2 = (
    *valid_stream_scenarios,
    *valid_timelimit_scenarios,
)
