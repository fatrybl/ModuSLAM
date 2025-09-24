"""Tests scenarios for Kaist Urban dataset."""

from moduslam.utils.exceptions import UnfeasibleRequestError
from tests.moduslam.data_manager.batch_factory.test_cases.kaist.data import (
    all_elements_batch,
    all_imu_batch,
    all_lidar2D_batch,
    all_stereo_batch,
    batch1,
    batch2,
    batch3,
    batch_factory_config1,
    batch_factory_config2,
    batch_factory_config3,
    batch_factory_config4,
    batch_factory_config5,
    batch_factory_config6,
    el3,
    el5,
    el10,
    el14,
    el19,
    el22,
    el23,
    el24,
    el25,
    elements,
    imu_batch_1,
    imu_batch_2,
    imu_batch_3,
    imu_request1,
    imu_request2,
    imu_request3,
    lidar2D_request1,
    lidar2D_request2,
    lidar2D_request3,
    lidar_2D_batch_1,
    lidar_2D_batch_2,
    sensors_factory_config1,
    sensors_factory_config2,
    stereo_batch_1,
    stereo_batch_2,
    stereo_request1,
    stereo_request2,
    stereo_request3,
)

kaist_scenarios1_success = (
    (sensors_factory_config1, batch_factory_config1, all_elements_batch),
    (sensors_factory_config1, batch_factory_config2, all_elements_batch),
    (sensors_factory_config1, batch_factory_config3, batch1),
    (sensors_factory_config1, batch_factory_config4, batch2),
    (sensors_factory_config1, batch_factory_config5, batch3),
    (sensors_factory_config2, batch_factory_config1, all_imu_batch),
    (sensors_factory_config2, batch_factory_config2, all_imu_batch),
    (sensors_factory_config2, batch_factory_config5, imu_batch_2),
)

kaist_scenarios1_fail = (sensors_factory_config1, batch_factory_config6)

kaist_scenarios2_success = (
    (sensors_factory_config1, batch_factory_config1, elements, all_elements_batch),
    (sensors_factory_config1, batch_factory_config1, [el3], imu_batch_1),
    (sensors_factory_config1, batch_factory_config2, [el3, el3], imu_batch_1),
    (sensors_factory_config1, batch_factory_config1, [el10, el23, el23], imu_batch_2),
    (sensors_factory_config1, batch_factory_config1, [el5], lidar_2D_batch_1),
    (sensors_factory_config1, batch_factory_config1, [el5, el14, el25], all_lidar2D_batch),
    (sensors_factory_config1, batch_factory_config1, [el19], stereo_batch_1),
    (sensors_factory_config1, batch_factory_config1, [el19, el22, el24], all_stereo_batch),
)

kaist_scenarios2_fail = (sensors_factory_config1, batch_factory_config6, elements)

kaist_scenarios3_success = (
    (sensors_factory_config1, batch_factory_config2, imu_request1, imu_batch_1),
    (sensors_factory_config1, batch_factory_config2, imu_request2, imu_batch_3),
    (sensors_factory_config2, batch_factory_config5, imu_request2, imu_batch_3),
    (sensors_factory_config1, batch_factory_config2, imu_request3, all_imu_batch),
    (sensors_factory_config1, batch_factory_config2, lidar2D_request1, lidar_2D_batch_1),
    (sensors_factory_config1, batch_factory_config2, lidar2D_request2, lidar_2D_batch_2),
    (sensors_factory_config1, batch_factory_config2, lidar2D_request3, all_lidar2D_batch),
    (sensors_factory_config1, batch_factory_config2, stereo_request1, stereo_batch_1),
    (sensors_factory_config1, batch_factory_config2, stereo_request2, stereo_batch_2),
    (sensors_factory_config1, batch_factory_config1, stereo_request3, all_stereo_batch),
)

kaist_scenarios3_fail = (
    (sensors_factory_config1, batch_factory_config4, imu_request1, UnfeasibleRequestError),
    (sensors_factory_config1, batch_factory_config5, lidar2D_request1, UnfeasibleRequestError),
    (sensors_factory_config2, batch_factory_config1, stereo_request1, UnfeasibleRequestError),
)
