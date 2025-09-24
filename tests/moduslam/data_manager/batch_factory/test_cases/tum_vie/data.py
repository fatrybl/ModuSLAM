from moduslam.data_manager.batch_factory.batch import DataBatch
from moduslam.data_manager.batch_factory.configs import (
    BatchFactoryConfig,
    DataRegimeConfig,
)
from moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.utils.auxiliary_dataclasses import PeriodicDataRequest, TimeRange
from moduslam.utils.auxiliary_methods import nanosec2microsec
from tests.conftest import tum_vie_dataset_dir
from tests.tests_data_generators.tum_vie_dataset.data import Data
from tests.tests_data_generators.utils import generate_sensors_factory_config

dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
data = Data(dataset_cfg)
elements = data.elements

imu = data.imu
stereo = data.stereo

empty_batch = DataBatch()

all_elements_batch = DataBatch()
for element in elements:
    all_elements_batch.add(element)

el1 = elements[0]
el2 = elements[1]
el15 = elements[14]
el23 = elements[22]
el24 = elements[23]
different_elements = elements[1:15]

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

imu_batch_1 = DataBatch()
imu_batch_1.add(el2)

imu_batch_2 = DataBatch()
imu_batch_2.add(el23)

all_imu_batch = DataBatch()
for element in elements:
    if element.measurement.sensor == imu:
        all_imu_batch.add(element)

stereo_batch_1 = DataBatch()
stereo_batch_1.add(el1)

stereo_batch_2 = DataBatch()
stereo_batch_2.add(el24)

all_stereo_batch = DataBatch()
for element in elements:
    if element.measurement.sensor == stereo:
        all_stereo_batch.add(element)

batch_1 = DataBatch()
for element in different_elements:
    batch_1.add(element)

batch_2 = DataBatch()
batch_2.add(el2)
batch_2.add(el24)

imu_request1 = PeriodicDataRequest(
    sensor=el2.measurement.sensor, period=TimeRange(start=el2.timestamp, stop=el2.timestamp)
)
imu_request2 = PeriodicDataRequest(
    sensor=el23.measurement.sensor, period=TimeRange(start=el23.timestamp, stop=el23.timestamp)
)
imu_request3 = PeriodicDataRequest(
    sensor=el2.measurement.sensor, period=TimeRange(start=el2.timestamp, stop=el23.timestamp)
)

stereo_request1 = PeriodicDataRequest(
    sensor=el1.measurement.sensor, period=TimeRange(start=el1.timestamp, stop=el1.timestamp)
)
stereo_request2 = PeriodicDataRequest(
    sensor=el24.measurement.sensor, period=TimeRange(start=el24.timestamp, stop=el24.timestamp)
)
stereo_request3 = PeriodicDataRequest(
    sensor=el1.measurement.sensor, period=TimeRange(start=el1.timestamp, stop=el24.timestamp)
)
