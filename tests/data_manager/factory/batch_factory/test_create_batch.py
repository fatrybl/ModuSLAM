from collections import deque

from pytest import mark

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.element import Element
from slam.setup_manager.sensors_factory.factory import SensorFactory
from slam.system_configs.system.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from slam.system_configs.system.setup_manager.sensors_factory import SensorFactoryConfig
from slam.utils.auxiliary_dataclasses import PeriodicData
from slam.utils.auxiliary_methods import equal_elements
from tests.data_manager.factory.batch_factory.scenarios import sc1, sc2, sc3

test_cases_1 = (*sc1,)
test_cases_2 = (*sc2,)
test_cases_3 = (*sc3,)


class TestBatchFactory:

    @mark.parametrize("config1, config2, reference_batch", [*test_cases_1])
    def test_create_batch_1(
        self,
        config1: SensorFactoryConfig,
        config2: BatchFactoryConfig,
        reference_batch: DataBatch,
    ):
        SensorFactory.init_sensors(config1)

        batch_factory = BatchFactory(config2)

        batch_factory.create_batch()
        result_batch: DataBatch = batch_factory.batch

        for result, reference in zip(result_batch.data, reference_batch.data):
            equal_elements(result, reference)

    @mark.parametrize("config1, config2, reference_batch", [*test_cases_2])
    def test_create_batch_2(
        self,
        config1: SensorFactoryConfig,
        config2: BatchFactoryConfig,
        reference_batch: DataBatch,
    ):
        SensorFactory.init_sensors(config1)

        batch_factory = BatchFactory(config2)

        elements: deque[Element] = reference_batch.data

        batch_factory.create_batch(elements)
        result_batch: DataBatch = batch_factory.batch

        for result, reference in zip(result_batch.data, reference_batch.data):
            equal_elements(result, reference)

    @mark.parametrize("config1, config2, periodic_data_requests, reference_batch", [*test_cases_3])
    def test_create_batch_3(
        self,
        config1: SensorFactoryConfig,
        config2: BatchFactoryConfig,
        periodic_data_requests: set[PeriodicData],
        reference_batch: DataBatch,
    ):

        SensorFactory.init_sensors(config1)
        batch_factory = BatchFactory(config2)

        batch_factory.create_batch(periodic_data_requests)

        result_batch: DataBatch = batch_factory.batch

        for result, reference in zip(result_batch.data, reference_batch.data):
            equal_elements(result, reference)
