"""Test data for the tests of the BatchFactory class."""

import itertools

from moduslam.data_manager.batch_factory.batch import DataBatch
from moduslam.data_manager.batch_factory.configs import (
    BatchFactoryConfig,
    DataRegimeConfig,
)
from moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2HumbleConfig,
)
from moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.utils.auxiliary_dataclasses import PeriodicDataRequest, TimeRange
from tests.conftest import s3e_dataset_dir
from tests.tests_data_generators.ros2.s3e_dataset.data import (
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

dataset_cfg = Ros2HumbleConfig(
    directory=s3e_dataset_dir, sensor_topic_mapping=sensor_name_topic_map
)

sensors_configs_1 = [imu_cfg, lidar_cfg, left_camera_cfg, right_camera_cfg, rtk_cfg]
sensors_configs_2 = [imu_cfg]
sensors_configs_3 = [left_camera_cfg, lidar_cfg]

full_memory_percent = 100.0
low_memory_percent = 1.0

stream = DataRegimeConfig(name=Stream.name)

t_limit_1 = DataRegimeConfig(
    TimeLimit.name, start=str(elements[0].timestamp), stop=str(elements[-1].timestamp)
)
t_limit_2 = DataRegimeConfig(
    TimeLimit.name, start=str(elements[0].timestamp), stop=str(elements[9].timestamp)
)
t_limit_3 = DataRegimeConfig(
    TimeLimit.name, start=str(elements[10].timestamp), stop=str(elements[-1].timestamp)
)
t_limit_4 = DataRegimeConfig(
    TimeLimit.name, start=str(imu_elements[0].timestamp), stop=str(imu_elements[-1].timestamp)
)
t_limit_5 = DataRegimeConfig(
    TimeLimit.name,
    start=str(left_camera_lidar_elements[0].timestamp),
    stop=str(left_camera_lidar_elements[-1].timestamp),
)
t_limit_6 = DataRegimeConfig(
    TimeLimit.name, start=str(lidar_elements[0].timestamp), stop=str(lidar_elements[0].timestamp)
)
t_limit_7 = DataRegimeConfig(
    TimeLimit.name, start=str(imu_elements[5].timestamp), stop=str(imu_elements[10].timestamp)
)

batch_factory_config1 = BatchFactoryConfig(dataset_cfg, stream, full_memory_percent)
batch_factory_config2 = BatchFactoryConfig(dataset_cfg, t_limit_1, full_memory_percent)
batch_factory_config3 = BatchFactoryConfig(dataset_cfg, t_limit_2, full_memory_percent)
batch_factory_config4 = BatchFactoryConfig(dataset_cfg, t_limit_3, full_memory_percent)
batch_factory_config5 = BatchFactoryConfig(dataset_cfg, t_limit_4, full_memory_percent)
batch_factory_config6 = BatchFactoryConfig(dataset_cfg, t_limit_5, full_memory_percent)
batch_factory_config7 = BatchFactoryConfig(dataset_cfg, t_limit_6, full_memory_percent)
batch_factory_config8 = BatchFactoryConfig(dataset_cfg, t_limit_7, full_memory_percent)
batch_factory_config9 = BatchFactoryConfig(dataset_cfg, stream, low_memory_percent)

empty_batch = DataBatch()

all_elements_batch = DataBatch()
for el in elements:
    all_elements_batch.add(el)

batch1 = DataBatch()
for el in itertools.islice(elements, 0, 10):  # first 10 elements
    batch1.add(el)

batch2 = DataBatch()
for el in itertools.islice(elements, 10, 20):  # last 10 elements
    batch2.add(el)

batch3 = DataBatch()
for el in itertools.islice(imu_elements, 5, 11):  # 5-11 elements
    batch3.add(el)

imu_batch = DataBatch()
for el in imu_elements:
    imu_batch.add(el)

lidar_batch = DataBatch()
for el in lidar_elements:
    lidar_batch.add(el)

left_camera_batch = DataBatch()
for el in left_camera_elements:
    left_camera_batch.add(el)

left_camera_lidar_batch = DataBatch()
for el in left_camera_lidar_elements:
    left_camera_lidar_batch.add(el)

one_element_batch = DataBatch()
one_element_batch.add(lidar_elements[0])

imu_request = PeriodicDataRequest(
    sensor=imu, period=TimeRange(start=imu_elements[0].timestamp, stop=imu_elements[-1].timestamp)
)

lidar_request = PeriodicDataRequest(
    sensor=lidar,
    period=TimeRange(start=lidar_elements[0].timestamp, stop=lidar_elements[-1].timestamp),
)

left_camera_request = PeriodicDataRequest(
    sensor=left_camera,
    period=TimeRange(
        start=left_camera_elements[0].timestamp, stop=left_camera_elements[-1].timestamp
    ),
)

mid_imu_request = PeriodicDataRequest(
    sensor=imu, period=TimeRange(start=imu_elements[5].timestamp, stop=imu_elements[10].timestamp)
)
