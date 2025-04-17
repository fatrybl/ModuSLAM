"""Tests scenarios for Ros-2 S3E dataset."""

from src.tests.moduslam.data_manager.batch_factory.test_cases.ros2.s3e_data import (
    all_elements_batch,
    batch1,
    batch2,
    batch3,
    batch_factory_config1,
    batch_factory_config2,
    batch_factory_config3,
    batch_factory_config4,
    batch_factory_config5,
    batch_factory_config6,
    batch_factory_config7,
    batch_factory_config8,
    batch_factory_config9,
    elements,
    empty_batch,
    imu_batch,
    imu_request,
    left_camera_batch,
    left_camera_lidar_batch,
    left_camera_lidar_elements,
    left_camera_request,
    lidar_batch,
    lidar_elements,
    lidar_request,
    mid_imu_request,
    one_element_batch,
    sensors_configs_1,
    sensors_configs_2,
    sensors_configs_3,
)
from src.utils.exceptions import UnfeasibleRequestError

ros2_s3e_scenarios1_success = (
    (sensors_configs_1, batch_factory_config1, all_elements_batch),
    (sensors_configs_1, batch_factory_config2, all_elements_batch),
    (sensors_configs_1, batch_factory_config3, batch1),
    (sensors_configs_1, batch_factory_config4, batch2),
    (sensors_configs_2, batch_factory_config5, imu_batch),
    (sensors_configs_3, batch_factory_config6, left_camera_lidar_batch),
    (sensors_configs_2, batch_factory_config7, empty_batch),
)

ros2_s3e_scenarios1_fail = (sensors_configs_1, batch_factory_config9)

ros2_s3e_scenarios2_success = (
    (sensors_configs_1, batch_factory_config1, elements, all_elements_batch),
    (sensors_configs_1, batch_factory_config7, elements, all_elements_batch),
    (sensors_configs_1, batch_factory_config1, [lidar_elements[0]], one_element_batch),
    (sensors_configs_2, batch_factory_config7, left_camera_lidar_elements, left_camera_lidar_batch),
)

ros2_s3e_scenarios2_fail = (sensors_configs_1, batch_factory_config9, elements)

ros2_s3e_scenarios3_success = (
    (sensors_configs_1, batch_factory_config1, imu_request, imu_batch),
    (sensors_configs_1, batch_factory_config1, lidar_request, lidar_batch),
    (sensors_configs_1, batch_factory_config1, left_camera_request, left_camera_batch),
    (sensors_configs_2, batch_factory_config8, mid_imu_request, batch3),
)

ros2_s3e_scenarios3_fail = (
    (sensors_configs_1, batch_factory_config7, imu_request, UnfeasibleRequestError),
    (sensors_configs_2, batch_factory_config8, lidar_request, UnfeasibleRequestError),
    (sensors_configs_3, batch_factory_config7, imu_request, UnfeasibleRequestError),
    (sensors_configs_1, batch_factory_config9, lidar_request, MemoryError),
)
