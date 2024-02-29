"""
WARNING:
    If PeriodicData request is out of TimeRange margins,
    the BatchFactory is still able to create a batch with the data that is in the TimeRange.
"""

from slam.system_configs.system.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from slam.system_configs.system.data_manager.batch_factory.memory import (
    MemoryAnalyzerConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import (
    RegimeConfig,
    Stream,
    TimeLimit,
)
from slam.system_configs.system.setup_manager.sensors_factory import SensorFactoryConfig
from tests.data_manager.factory.batch_factory.test_data.readers.kaist.batches import (
    all_elements_batch,
    common_batch,
    common_requests,
    imu_batch,
    imu_requests,
    lidar2D_batch,
    lidar2D_requests,
    stereo_batch,
    stereo_requests,
    t_range_1,
    t_range_2,
    t_range_3,
    t_range_4,
    time_limit_batches,
    time_limit_request_scenarios,
)
from tests_data.kaist_urban_dataset.data import DATASET_DIR, sensor_factory_cfg

dataset_cfg = KaistConfig(directory=DATASET_DIR)
memory_cfg = MemoryAnalyzerConfig(batch_memory=100)

cfg1: SensorFactoryConfig = sensor_factory_cfg

cfg2_stream = BatchFactoryConfig(
    memory=memory_cfg, dataset=dataset_cfg, regime=RegimeConfig(name=Stream.name)
)

t_limit_1 = RegimeConfig(name=TimeLimit.name, start=t_range_1.start, stop=t_range_1.stop)
t_limit_2 = RegimeConfig(name=TimeLimit.name, start=t_range_2.start, stop=t_range_2.stop)
t_limit_3 = RegimeConfig(name=TimeLimit.name, start=t_range_3.start, stop=t_range_3.stop)
t_limit_4 = RegimeConfig(name=TimeLimit.name, start=t_range_4.start, stop=t_range_4.stop)

cfg2_timelimit_1 = BatchFactoryConfig(memory=memory_cfg, dataset=dataset_cfg, regime=t_limit_1)
cfg2_timelimit_2 = BatchFactoryConfig(memory=memory_cfg, dataset=dataset_cfg, regime=t_limit_2)
cfg2_timelimit_3 = BatchFactoryConfig(memory=memory_cfg, dataset=dataset_cfg, regime=t_limit_3)
cfg2_timelimit_4 = BatchFactoryConfig(memory=memory_cfg, dataset=dataset_cfg, regime=t_limit_4)

scenarios = (
    (cfg1, cfg2_stream, all_elements_batch),
    (cfg1, cfg2_timelimit_1, time_limit_batches[0]),
    (cfg1, cfg2_timelimit_2, time_limit_batches[1]),
    (cfg1, cfg2_timelimit_3, time_limit_batches[2]),
    (cfg1, cfg2_timelimit_4, time_limit_batches[3]),
)


scenarios_periodic_data = (
    (cfg1, cfg2_stream, common_requests, common_batch),
    (cfg1, cfg2_stream, imu_requests, imu_batch),
    (cfg1, cfg2_stream, lidar2D_requests, lidar2D_batch),
    (cfg1, cfg2_stream, stereo_requests, stereo_batch),
    (cfg1, cfg2_timelimit_1, common_requests, common_batch),
    (cfg1, cfg2_timelimit_1, imu_requests, imu_batch),
    (cfg1, cfg2_timelimit_1, lidar2D_requests, lidar2D_batch),
    (cfg1, cfg2_timelimit_1, stereo_requests, stereo_batch),
    (cfg1, cfg2_timelimit_1, *time_limit_request_scenarios[0]),
    (cfg1, cfg2_timelimit_1, *time_limit_request_scenarios[1]),
    (cfg1, cfg2_timelimit_1, *time_limit_request_scenarios[2]),
    (cfg1, cfg2_timelimit_1, *time_limit_request_scenarios[3]),
)
