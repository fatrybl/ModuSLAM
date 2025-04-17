from src.tests.moduslam.data_manager.batch_factory.readers.ros2.scenarios.s3e_data import (
    all_sensors,
    dataset_cfg,
    elements,
    imu_elements,
    imu_list,
    left_camera_elements,
    left_camera_lidar_elements,
    left_camera_lidar_sensors,
    lidar_elements,
    lidar_list,
    sensors_configs_1,
    sensors_configs_2,
    sensors_configs_3,
    stream,
    t_limit_1,
    t_limit_2,
    t_limit_7,
    t_limit_8,
    t_limit_9,
    t_limit_10,
    t_limit_11,
)
from src.tests_data_generators.ros2.s3e_dataset.data import imu, left_camera, lidar

valid_stream_scenarios = (
    (sensors_configs_1, dataset_cfg, stream, all_sensors, elements),
    (sensors_configs_1, dataset_cfg, stream, imu_list, imu_elements),
    (sensors_configs_1, dataset_cfg, stream, lidar_list, lidar_elements),
    (
        sensors_configs_1,
        dataset_cfg,
        stream,
        left_camera_lidar_sensors,
        left_camera_lidar_elements,
    ),
    (sensors_configs_2, dataset_cfg, stream, imu_list, imu_elements),
    (
        sensors_configs_3,
        dataset_cfg,
        stream,
        left_camera_lidar_sensors,
        left_camera_lidar_elements,
    ),
    (sensors_configs_1, dataset_cfg, stream, all_sensors, [*elements, None]),
)

valid_timelimit_scenarios = (
    (sensors_configs_1, dataset_cfg, t_limit_1, all_sensors, elements),
    (sensors_configs_2, dataset_cfg, t_limit_7, imu_list, imu_elements),
    (sensors_configs_3, dataset_cfg, t_limit_8, lidar_list, lidar_elements),
    (
        sensors_configs_3,
        dataset_cfg,
        t_limit_9,
        left_camera_lidar_sensors,
        left_camera_lidar_elements,
    ),
    (
        sensors_configs_3,
        dataset_cfg,
        t_limit_10,
        [left_camera, left_camera],
        left_camera_elements[:2],
    ),
    (sensors_configs_1, dataset_cfg, t_limit_2, [left_camera, left_camera], [None, None]),
    (sensors_configs_1, dataset_cfg, t_limit_11, [imu, lidar], [imu_elements[0], None]),
    (sensors_configs_1, dataset_cfg, t_limit_2, [lidar, lidar], [lidar_elements[0], None]),
)

S3E_2 = (
    *valid_stream_scenarios,
    *valid_timelimit_scenarios,
)
