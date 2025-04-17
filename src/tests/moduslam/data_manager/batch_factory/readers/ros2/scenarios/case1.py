from src.tests.moduslam.data_manager.batch_factory.readers.ros2.scenarios.s3e_data import (
    dataset_cfg,
    elements,
    imu_elements,
    left_camera_lidar_elements,
    sensors_configs_1,
    sensors_configs_2,
    sensors_configs_3,
    stream,
    t_limit_1,
    t_limit_2,
    t_limit_3,
    t_limit_4,
    t_limit_5,
    t_limit_6,
)

valid_stream_scenarios = (
    (sensors_configs_1, dataset_cfg, stream, elements),
    (sensors_configs_2, dataset_cfg, stream, imu_elements),
    (sensors_configs_3, dataset_cfg, stream, left_camera_lidar_elements),
    (sensors_configs_2, dataset_cfg, stream, [*imu_elements, None]),
    (sensors_configs_1, dataset_cfg, stream, [*elements, None]),
)

valid_timelimit_scenarios = (
    (sensors_configs_1, dataset_cfg, t_limit_1, elements),
    (sensors_configs_1, dataset_cfg, t_limit_2, [elements[0]]),
    (sensors_configs_1, dataset_cfg, t_limit_3, [elements[-1]]),
    (sensors_configs_1, dataset_cfg, t_limit_4, elements[:-10]),
    (sensors_configs_1, dataset_cfg, t_limit_5, elements[10:]),
    (sensors_configs_1, dataset_cfg, t_limit_6, elements[5:15]),
    (sensors_configs_2, dataset_cfg, t_limit_1, imu_elements),
    (sensors_configs_3, dataset_cfg, t_limit_1, left_camera_lidar_elements),
    (sensors_configs_1, dataset_cfg, t_limit_1, [*elements, None]),
)

S3E_1 = (
    *valid_stream_scenarios,
    *valid_timelimit_scenarios,
)
