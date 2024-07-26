"""Tests scenarios for TumVie dataset."""

from moduslam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import (
    DataRegimeConfig,
    Stream,
    TimeLimit,
)
from moduslam.utils.auxiliary_methods import nanosec2microsec
from moduslam.utils.exceptions import UnfeasibleRequestError
from tests.conftest import tum_vie_dataset_dir
from tests.data_manager.batch_factory.test_cases.tum_vie.data import (
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
    empty_batch,
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
from tests_data_generators.utils import generate_sensors_factory_config

dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)

sensors_factory_config1 = generate_sensors_factory_config([imu, stereo])
sensors_factory_config2 = generate_sensors_factory_config([imu])
sensors_factory_config3 = generate_sensors_factory_config([stereo])
invalid_sensors_factory_config = generate_sensors_factory_config([])

stream = DataRegimeConfig(name=Stream.name)
t_limit_1 = DataRegimeConfig(
    TimeLimit.name, start=nanosec2microsec(el1.timestamp), stop=nanosec2microsec(el24.timestamp)
)
t_limit_2 = DataRegimeConfig(
    TimeLimit.name, start=nanosec2microsec(el1.timestamp), stop=nanosec2microsec(el1.timestamp)
)
t_limit_3 = DataRegimeConfig(
    TimeLimit.name, start=nanosec2microsec(el24.timestamp), stop=nanosec2microsec(el24.timestamp)
)
t_limit_4 = DataRegimeConfig(
    TimeLimit.name, start=nanosec2microsec(el2.timestamp), stop=nanosec2microsec(el15.timestamp)
)
t_limit_5 = DataRegimeConfig(
    TimeLimit.name, start=nanosec2microsec(el2.timestamp), stop=nanosec2microsec(el2.timestamp)
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
    (sensors_factory_config2, batch_factory_config3, empty_batch),
    (sensors_factory_config3, batch_factory_config6, empty_batch),
    (sensors_factory_config2, batch_factory_config1, all_imu_batch),
    (sensors_factory_config3, batch_factory_config1, all_stereo_batch),
    (invalid_sensors_factory_config, batch_factory_config1, empty_batch),
    (invalid_sensors_factory_config, batch_factory_config2, empty_batch),
)

tum_vie_scenarios1_fail = ((sensors_factory_config1, batch_factory_config7),)

tum_vie_scenarios2_success = (
    (sensors_factory_config1, batch_factory_config1, elements, all_elements_batch),
    (sensors_factory_config1, batch_factory_config2, elements, all_elements_batch),
    (sensors_factory_config2, batch_factory_config3, [el2], imu_batch_1),
    (sensors_factory_config3, batch_factory_config6, [el24], stereo_batch_2),
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
    (sensors_factory_config1, batch_factory_config7, imu_request1, MemoryError),
    (sensors_factory_config2, batch_factory_config1, stereo_request1, UnfeasibleRequestError),
    (sensors_factory_config3, batch_factory_config1, imu_request1, UnfeasibleRequestError),
    (sensors_factory_config2, batch_factory_config6, stereo_request1, UnfeasibleRequestError),
    (
        invalid_sensors_factory_config,
        batch_factory_config1,
        stereo_request1,
        UnfeasibleRequestError,
    ),
)
