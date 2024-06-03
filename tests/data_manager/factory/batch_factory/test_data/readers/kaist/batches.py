"""Test cases for Stream regime."""

import itertools

from moduslam.data_manager.factory.batch import DataBatch
from moduslam.data_manager.factory.element import Element
from moduslam.utils.auxiliary_dataclasses import PeriodicDataRequest, TimeRange
from tests_data.kaist_urban_dataset.data import (
    el1,
    el2,
    el3,
    el4,
    el5,
    el6,
    el7,
    el8,
    el9,
    el10,
    el11,
    el12,
    el13,
    el14,
    el15,
    el16,
    el17,
    el18,
    el19,
    el20,
    el21,
    el22,
    el23,
    el24,
    el25,
)

imu_requests: set[PeriodicDataRequest] = {
    PeriodicDataRequest(
        sensor=el3.measurement.sensor,
        period=TimeRange(start=el3.timestamp, stop=el3.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el10.measurement.sensor,
        period=TimeRange(start=el10.timestamp, stop=el10.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el23.measurement.sensor,
        period=TimeRange(start=el23.timestamp, stop=el23.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el3.measurement.sensor,
        period=TimeRange(start=el3.timestamp, stop=el23.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el3.measurement.sensor,
        period=TimeRange(start=el3.timestamp, stop=el10.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el10.measurement.sensor,
        period=TimeRange(start=el10.timestamp, stop=el23.timestamp),
    ),
}

imu_batch = DataBatch()
imu_batch.add(el3)
imu_batch.add(el10)
imu_batch.add(el23)


lidar2D_requests: set[PeriodicDataRequest] = {
    PeriodicDataRequest(
        sensor=el5.measurement.sensor,
        period=TimeRange(start=el5.timestamp, stop=el5.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el14.measurement.sensor,
        period=TimeRange(start=el14.timestamp, stop=el14.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el25.measurement.sensor,
        period=TimeRange(start=el25.timestamp, stop=el25.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el5.measurement.sensor,
        period=TimeRange(start=el5.timestamp, stop=el25.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el5.measurement.sensor,
        period=TimeRange(start=el5.timestamp, stop=el14.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el14.measurement.sensor,
        period=TimeRange(start=el14.timestamp, stop=el25.timestamp),
    ),
}

lidar2D_batch = DataBatch()
lidar2D_batch.add(el5)
lidar2D_batch.add(el14)
lidar2D_batch.add(el25)


stereo_requests: set[PeriodicDataRequest] = {
    PeriodicDataRequest(
        sensor=el19.measurement.sensor,
        period=TimeRange(start=el19.timestamp, stop=el19.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el22.measurement.sensor,
        period=TimeRange(start=el22.timestamp, stop=el22.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el24.measurement.sensor,
        period=TimeRange(start=el24.timestamp, stop=el24.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el19.measurement.sensor,
        period=TimeRange(start=el19.timestamp, stop=el24.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el19.measurement.sensor,
        period=TimeRange(start=el19.timestamp, stop=el22.timestamp),
    ),
    PeriodicDataRequest(
        sensor=el22.measurement.sensor,
        period=TimeRange(start=el22.timestamp, stop=el24.timestamp),
    ),
}

stereo_batch = DataBatch()
stereo_batch.add(el19)
stereo_batch.add(el22)
stereo_batch.add(el24)

common_batch = DataBatch()
for el in [el3, el5, el10, el14, el19, el22, el23, el24, el25]:
    common_batch.add(el)

common_requests = {*imu_requests, *lidar2D_requests, *stereo_requests}

imu_scenario: tuple[set[PeriodicDataRequest], DataBatch] = (imu_requests, imu_batch)
lidar2D_scenario: tuple[set[PeriodicDataRequest], DataBatch] = (
    lidar2D_requests,
    lidar2D_batch,
)
stereo_scenario: tuple[set[PeriodicDataRequest], DataBatch] = (stereo_requests, stereo_batch)
common_scenario: tuple[set[PeriodicDataRequest], DataBatch] = (common_requests, common_batch)

kaist_dataset_requests_scenarios: list[tuple[set[PeriodicDataRequest], DataBatch]] = [
    imu_scenario,
    lidar2D_scenario,
    stereo_scenario,
    common_scenario,
]


elements: list[Element] = [
    el1,
    el2,
    el3,
    el4,
    el5,
    el6,
    el7,
    el8,
    el9,
    el10,
    el11,
    el12,
    el13,
    el14,
    el15,
    el16,
    el17,
    el18,
    el19,
    el20,
    el21,
    el22,
    el23,
    el24,
    el25,
]
all_elements_batch = DataBatch()
for el in elements:
    all_elements_batch.add(el)


"""
Test cases for TimeLimit regime.
"""

b1 = DataBatch()
b2 = DataBatch()
b3 = DataBatch()
b4 = DataBatch()
b5 = DataBatch()


b1.add(el1)
b2.add(el25)

for el in itertools.islice(elements, el9.timestamp, el20.timestamp):
    b3.add(el)

for el in [el3, el10, el23]:
    b4.add(el)

for el in [el1, el3, el10, el23, el25]:
    b5.add(el)

t_range_1 = TimeRange(el1.timestamp, el25.timestamp)
t_range_2 = TimeRange(el1.timestamp, el1.timestamp)
t_range_3 = TimeRange(el25.timestamp, el25.timestamp)
t_range_4 = TimeRange(el10.timestamp, el20.timestamp)
t_range_5 = TimeRange(el3.timestamp, el23.timestamp)

time_limit_batches: list[DataBatch] = [all_elements_batch, b1, b2, b3]

request1 = PeriodicDataRequest(sensor=el1.measurement.sensor, period=t_range_2)
request2 = PeriodicDataRequest(sensor=el25.measurement.sensor, period=t_range_3)
request3 = PeriodicDataRequest(sensor=el3.measurement.sensor, period=t_range_5)
all_requests: set[PeriodicDataRequest] = {request1, request2, request3}


time_limit_request_scenarios: list[tuple[set[PeriodicDataRequest], DataBatch]] = [
    ({request1}, b1),
    ({request2}, b2),
    ({request3}, b4),
    (all_requests, b5),
]
