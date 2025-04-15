"""Tests scenarios for Tum Vie dataset."""

from src.moduslam.data_manager.batch_factory.configs import (
    BatchFactoryConfig,
    DataRegimeConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.tests.conftest import tum_vie_dataset_dir
from src.tests.moduslam.data_manager.batch_factory.test_cases.tum_vie.data import (
    all_elements_batch,
    all_imu_batch,
    all_stereo_batch,
    batch_1,
    batch_2,
    different_elements,
    el1,
    el2,
    el15,
    el24,
    elements,
    imu,
    imu_batch_1,
    imu_batch_2,
    imu_request1,
    imu_request2,
    imu_request3,
    stereo,
    stereo_batch_1,
    stereo_batch_2,
    stereo_request1,
    stereo_request2,
    stereo_request3,
)
from src.tests_data_generators.utils import generate_sensors_factory_config
from src.utils.auxiliary_methods import nanosec2microsec
from src.utils.exceptions import UnfeasibleRequestError

dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)

sensors_factory_config1 = generate_sensors_factory_config([imu, stereo])
sensors_factory_config2 = generate_sensors_factory_config([imu])
sensors_factory_config3 = generate_sensors_factory_config([stereo])

stream = DataRegimeConfig(name=Stream.name)
t_limit_1 = DataRegimeConfig(
    TimeLimit.name,
    start=str(nanosec2microsec(el1.timestamp)),
    stop=str(nanosec2microsec(el24.timestamp)),
)
t_limit_2 = DataRegimeConfig(
    TimeLimit.name,
    start=str(nanosec2microsec(el1.timestamp)),
    stop=str(nanosec2microsec(el1.timestamp)),
)
t_limit_3 = DataRegimeConfig(
    TimeLimit.name,
    start=str(nanosec2microsec(el24.timestamp)),
    stop=str(nanosec2microsec(el24.timestamp)),
)
t_limit_4 = DataRegimeConfig(
    TimeLimit.name,
    start=str(nanosec2microsec(el2.timestamp)),
    stop=str(nanosec2microsec(el15.timestamp)),
)
t_limit_5 = DataRegimeConfig(
    TimeLimit.name,
    start=str(nanosec2microsec(el2.timestamp)),
    stop=str(nanosec2microsec(el2.timestamp)),
)

full_memory_percent = 100.0
low_memory_percent = 1.0

batch_factory_config1 = BatchFactoryConfig(dataset_cfg, stream, full_memory_percent)
batch_factory_config2 = BatchFactoryConfig(dataset_cfg, t_limit_1, full_memory_percent)
batch_factory_config3 = BatchFactoryConfig(dataset_cfg, t_limit_2, full_memory_percent)
batch_factory_config4 = BatchFactoryConfig(dataset_cfg, t_limit_3, full_memory_percent)
batch_factory_config5 = BatchFactoryConfig(dataset_cfg, t_limit_4, full_memory_percent)
batch_factory_config6 = BatchFactoryConfig(dataset_cfg, t_limit_5, full_memory_percent)
batch_factory_config7 = BatchFactoryConfig(dataset_cfg, stream, low_memory_percent)

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

tum_vie_scenarios1_fail = ((sensors_factory_config1, batch_factory_config7),)

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

tum_vie_scenarios2_fail = ((sensors_factory_config1, batch_factory_config7, elements),)

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
