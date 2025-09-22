"""Tests scenarios for Tum Vie dataset."""

from moduslam.utils.exceptions import UnfeasibleRequestError
from tests.moduslam.data_manager.batch_factory.test_cases.tum_vie.data import (
    all_elements_batch,
    all_imu_batch,
    all_stereo_batch,
    batch_1,
    batch_2,
    batch_factory_config1,
    batch_factory_config2,
    batch_factory_config3,
    batch_factory_config4,
    batch_factory_config5,
    batch_factory_config6,
    batch_factory_config7,
    different_elements,
    el2,
    el24,
    elements,
    imu_batch_1,
    imu_batch_2,
    imu_request1,
    imu_request2,
    imu_request3,
    sensors_factory_config1,
    sensors_factory_config2,
    sensors_factory_config3,
    stereo_batch_1,
    stereo_batch_2,
    stereo_request1,
    stereo_request2,
    stereo_request3,
)

tum_vie_scenarios1_success = (
    (sensors_factory_config1, batch_factory_config1, all_elements_batch),
    (sensors_factory_config1, batch_factory_config2, all_elements_batch),
    (sensors_factory_config1, batch_factory_config3, stereo_batch_1),
    (sensors_factory_config1, batch_factory_config4, stereo_batch_2),
    (sensors_factory_config1, batch_factory_config5, batch_1),
    (sensors_factory_config2, batch_factory_config6, imu_batch_1),
    (sensors_factory_config3, batch_factory_config3, stereo_batch_1),
    (sensors_factory_config2, batch_factory_config1, all_imu_batch),
    (sensors_factory_config3, batch_factory_config1, all_stereo_batch),
)

tum_vie_scenarios1_fail = (sensors_factory_config1, batch_factory_config7)

tum_vie_scenarios2_success = (
    (sensors_factory_config1, batch_factory_config1, elements, all_elements_batch),
    (sensors_factory_config1, batch_factory_config2, elements, all_elements_batch),
    (sensors_factory_config2, batch_factory_config6, [el2], imu_batch_1),
    (sensors_factory_config3, batch_factory_config4, [el24], stereo_batch_2),
    (sensors_factory_config1, batch_factory_config1, [el2, el2], imu_batch_1),
    (sensors_factory_config1, batch_factory_config1, [el24, el24], stereo_batch_2),
    (sensors_factory_config1, batch_factory_config1, [el2, el2, el24, el24], batch_2),
    (sensors_factory_config1, batch_factory_config1, [el2, el24, el24], batch_2),
    (sensors_factory_config1, batch_factory_config1, different_elements, batch_1),
)

tum_vie_scenarios2_fail = (sensors_factory_config1, batch_factory_config7, elements)

tum_vie_scenarios3_success = (
    (sensors_factory_config1, batch_factory_config1, stereo_request1, stereo_batch_1),
    (sensors_factory_config1, batch_factory_config1, stereo_request2, stereo_batch_2),
    (sensors_factory_config1, batch_factory_config1, stereo_request3, all_stereo_batch),
    (sensors_factory_config1, batch_factory_config2, imu_request1, imu_batch_1),
    (sensors_factory_config1, batch_factory_config2, imu_request2, imu_batch_2),
    (sensors_factory_config1, batch_factory_config2, imu_request3, all_imu_batch),
)

tum_vie_scenarios3_fail = (
    (sensors_factory_config1, batch_factory_config6, stereo_request1, UnfeasibleRequestError),
    (sensors_factory_config2, batch_factory_config1, stereo_request1, UnfeasibleRequestError),
    (sensors_factory_config2, batch_factory_config6, imu_request2, UnfeasibleRequestError),
)
