"""Test data for the tests of the BatchFactory class."""

import itertools

from src.moduslam.data_manager.batch_factory.batch import DataBatch
from src.moduslam.data_manager.batch_factory.configs import (
    BatchFactoryConfig,
    DataRegimeConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.tests.conftest import kaist_custom_dataset_dir
from src.tests_data_generators.kaist_dataset.data import Data
from src.tests_data_generators.utils import generate_sensors_factory_config
from src.utils.auxiliary_dataclasses import PeriodicDataRequest, TimeRange

data = Data(kaist_custom_dataset_dir)
elements = data.elements

dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)

all_sensors = [element.measurement.sensor for element in elements]

full_memory_percent = 100.0
low_memory_percent = 1.0

imu = data.imu
lidar2D = data.sick_middle
stereo = data.stereo

el1 = elements[0]
el3 = elements[2]
el5 = elements[4]
el9 = elements[8]
el10 = elements[9]
el11 = elements[10]
el13 = elements[12]
el14 = elements[13]
el16 = elements[15]
el19 = elements[18]
el20 = elements[19]
el22 = elements[21]
el23 = elements[22]
el24 = elements[23]
el25 = elements[24]

sensors_factory_config1 = generate_sensors_factory_config(all_sensors)
sensors_factory_config2 = generate_sensors_factory_config([imu])

stream = DataRegimeConfig(name=Stream.name)
t_limit_1 = DataRegimeConfig(
    name=TimeLimit.name, start=str(el1.timestamp), stop=str(el25.timestamp)
)
t_limit_2 = DataRegimeConfig(name=TimeLimit.name, start=str(el1.timestamp), stop=str(el1.timestamp))
t_limit_3 = DataRegimeConfig(
    name=TimeLimit.name, start=str(el25.timestamp), stop=str(el25.timestamp)
)
t_limit_4 = DataRegimeConfig(
    name=TimeLimit.name, start=str(el10.timestamp), stop=str(el23.timestamp)
)

batch_factory_config1 = BatchFactoryConfig(dataset_cfg, stream, full_memory_percent)
batch_factory_config2 = BatchFactoryConfig(dataset_cfg, t_limit_1, full_memory_percent)
batch_factory_config3 = BatchFactoryConfig(dataset_cfg, t_limit_2, full_memory_percent)
batch_factory_config4 = BatchFactoryConfig(dataset_cfg, t_limit_3, full_memory_percent)
batch_factory_config5 = BatchFactoryConfig(dataset_cfg, t_limit_4, full_memory_percent)
batch_factory_config6 = BatchFactoryConfig(dataset_cfg, stream, low_memory_percent)

empty_batch = DataBatch()

all_elements_batch = DataBatch()
for el in elements:
    all_elements_batch.add(el)

imu_batch_1 = DataBatch()
imu_batch_1.add(el3)

imu_batch_2 = DataBatch()
imu_batch_2.add(el10)
imu_batch_2.add(el23)

imu_batch_3 = DataBatch()
imu_batch_3.add(el23)

all_imu_batch = DataBatch()
all_imu_batch.add(el3)
all_imu_batch.add(el10)
all_imu_batch.add(el23)

lidar_2D_batch_1 = DataBatch()
lidar_2D_batch_1.add(el5)

lidar_2D_batch_2 = DataBatch()
lidar_2D_batch_2.add(el25)

all_lidar2D_batch = DataBatch()
all_lidar2D_batch.add(el5)
all_lidar2D_batch.add(el14)
all_lidar2D_batch.add(el25)

stereo_batch_1 = DataBatch()
stereo_batch_1.add(el19)

stereo_batch_2 = DataBatch()
stereo_batch_2.add(el24)

all_stereo_batch = DataBatch()
all_stereo_batch.add(el19)
all_stereo_batch.add(el22)
all_stereo_batch.add(el24)

batch1 = DataBatch()
batch2 = DataBatch()
batch3 = DataBatch()
batch4 = DataBatch()
batch5 = DataBatch()

batch1.add(el1)
batch2.add(el25)

for el in itertools.islice(elements, el9.timestamp, el23.timestamp):
    batch3.add(el)

for el in [el3, el10, el23]:
    batch4.add(el)

for el in [el1, el3, el10, el23, el25]:
    batch5.add(el)

imu_request1 = PeriodicDataRequest(
    sensor=el3.measurement.sensor, period=TimeRange(start=el3.timestamp, stop=el3.timestamp)
)
imu_request2 = PeriodicDataRequest(
    sensor=el23.measurement.sensor, period=TimeRange(start=el23.timestamp, stop=el23.timestamp)
)
imu_request3 = PeriodicDataRequest(
    sensor=el3.measurement.sensor, period=TimeRange(start=el3.timestamp, stop=el23.timestamp)
)

lidar2D_request1 = PeriodicDataRequest(
    sensor=el5.measurement.sensor, period=TimeRange(start=el5.timestamp, stop=el5.timestamp)
)

lidar2D_request2 = PeriodicDataRequest(
    sensor=el25.measurement.sensor, period=TimeRange(start=el25.timestamp, stop=el25.timestamp)
)

lidar2D_request3 = PeriodicDataRequest(
    sensor=el5.measurement.sensor, period=TimeRange(start=el5.timestamp, stop=el25.timestamp)
)

stereo_request1 = PeriodicDataRequest(
    sensor=el19.measurement.sensor, period=TimeRange(start=el19.timestamp, stop=el19.timestamp)
)
stereo_request2 = PeriodicDataRequest(
    sensor=el24.measurement.sensor, period=TimeRange(start=el24.timestamp, stop=el24.timestamp)
)
stereo_request3 = PeriodicDataRequest(
    sensor=el19.measurement.sensor, period=TimeRange(start=el19.timestamp, stop=el24.timestamp)
)

invalid_request1 = PeriodicDataRequest(
    sensor=el16.measurement.sensor, period=TimeRange(start=el1.timestamp, stop=el10.timestamp)
)

invalid_request2 = PeriodicDataRequest(
    sensor=el3.measurement.sensor, period=TimeRange(start=el11.timestamp, stop=el13.timestamp)
)
