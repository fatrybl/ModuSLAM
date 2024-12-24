from phd.moduslam.data_manager.batch_factory.batch import DataBatch
from phd.moduslam.data_manager.batch_factory.readers.tum_vie.configs.base import (
    TumVieConfig,
)
from phd.tests.conftest import tum_vie_dataset_dir
from phd.tests_data_generators.tum_vie_dataset.data import Data
from phd.utils.auxiliary_dataclasses import PeriodicDataRequest, TimeRange

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
