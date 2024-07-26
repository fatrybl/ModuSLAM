"""Tests scenarios for Kaist dataset."""

from moduslam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import (
    DataRegimeConfig,
    Stream,
    TimeLimit,
)
from moduslam.utils.exceptions import UnfeasibleRequestError
from tests.conftest import kaist_custom_dataset_dir
from tests.data_manager.batch_factory.test_cases.kaist.data import (
    all_elements_batch,
    all_imu_batch,
    all_lidar2D_batch,
    all_stereo_batch,
    batch1,
    batch2,
    batch3,
    el1,
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
    empty_batch,
    imu,
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
    stereo_batch_1,
    stereo_batch_2,
    stereo_request1,
    stereo_request2,
    stereo_request3,
)
from tests_data_generators.utils import generate_sensors_factory_config

dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)

all_sensors = [element.measurement.sensor for element in elements]
sensors_factory_config1 = generate_sensors_factory_config(all_sensors)
sensors_factory_config2 = generate_sensors_factory_config([imu])
invalid_sensors_factory_config = generate_sensors_factory_config([])

stream = DataRegimeConfig(name=Stream.name)
t_limit_1 = DataRegimeConfig(name=TimeLimit.name, start=el1.timestamp, stop=el25.timestamp)
t_limit_2 = DataRegimeConfig(name=TimeLimit.name, start=el1.timestamp, stop=el1.timestamp)
t_limit_3 = DataRegimeConfig(name=TimeLimit.name, start=el25.timestamp, stop=el25.timestamp)
t_limit_4 = DataRegimeConfig(name=TimeLimit.name, start=el10.timestamp, stop=el23.timestamp)

full_memory_percent = 100.0
low_memory_percent = 1.0

batch_factory_config1 = BatchFactoryConfig(dataset_cfg, stream, full_memory_percent)
batch_factory_config2 = BatchFactoryConfig(dataset_cfg, t_limit_1, full_memory_percent)
batch_factory_config3 = BatchFactoryConfig(dataset_cfg, t_limit_2, full_memory_percent)
batch_factory_config4 = BatchFactoryConfig(dataset_cfg, t_limit_3, full_memory_percent)
batch_factory_config5 = BatchFactoryConfig(dataset_cfg, t_limit_4, full_memory_percent)
batch_factory_config6 = BatchFactoryConfig(dataset_cfg, stream, low_memory_percent)

kaist_scenarios1_success = (
    (sensors_factory_config1, batch_factory_config1, all_elements_batch),
    (sensors_factory_config1, batch_factory_config2, all_elements_batch),
    (sensors_factory_config1, batch_factory_config3, batch1),
    (sensors_factory_config1, batch_factory_config4, batch2),
    (sensors_factory_config1, batch_factory_config5, batch3),
    (sensors_factory_config2, batch_factory_config1, all_imu_batch),
    (sensors_factory_config2, batch_factory_config2, all_imu_batch),
    (sensors_factory_config2, batch_factory_config5, imu_batch_2),
    (sensors_factory_config2, batch_factory_config4, empty_batch),
    (invalid_sensors_factory_config, batch_factory_config1, empty_batch),
    (invalid_sensors_factory_config, batch_factory_config2, empty_batch),
)

kaist_scenarios1_fail = ((sensors_factory_config1, batch_factory_config6),)

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

kaist_scenarios2_fail = ((sensors_factory_config1, batch_factory_config6, elements),)


kaist_scenarios3_success = (
    (sensors_factory_config1, batch_factory_config2, imu_request1, imu_batch_1),
    (sensors_factory_config1, batch_factory_config2, imu_request2, imu_batch_3),
    (sensors_factory_config1, batch_factory_config2, imu_request3, all_imu_batch),
    (sensors_factory_config1, batch_factory_config2, lidar2D_request1, lidar_2D_batch_1),
    (sensors_factory_config1, batch_factory_config2, lidar2D_request2, lidar_2D_batch_2),
    (sensors_factory_config1, batch_factory_config2, lidar2D_request3, all_lidar2D_batch),
    (sensors_factory_config1, batch_factory_config2, stereo_request1, stereo_batch_1),
    (sensors_factory_config1, batch_factory_config2, stereo_request2, stereo_batch_2),
    (sensors_factory_config1, batch_factory_config1, stereo_request3, all_stereo_batch),
)


kaist_scenarios3_fail = (
    (sensors_factory_config1, batch_factory_config6, imu_request1, MemoryError),
    (sensors_factory_config2, batch_factory_config3, imu_request1, UnfeasibleRequestError),
    (invalid_sensors_factory_config, batch_factory_config2, imu_request1, UnfeasibleRequestError),
    (
        invalid_sensors_factory_config,
        batch_factory_config2,
        stereo_request1,
        UnfeasibleRequestError,
    ),
    (sensors_factory_config1, batch_factory_config5, lidar2D_request1, UnfeasibleRequestError),
)
