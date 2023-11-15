from collections import deque
from pytest import mark

from hydra import initialize_config_module, compose
from hydra.core.config_store import ConfigStore
from PIL.Image import Image

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.auxiliary_dataclasses import PeriodicData, TimeRange

from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory

from tests.data_manager.factory.batch_factory.conftest import CONFIG_MODULE_DIR, BATCH_FACTORY_CONFIG_NAME
from tests.data_manager.factory.batch_factory.conftest import Fixture

from .data import scenarios, periodic_request_scenarios, incorrect_scenario
from .config import BFConfig


class TestBatchFactoryKaistDataset:
    """
    Tests create_batch() method of a BatchFactory with Kaist Urban based dataset and "TimeLimit" regime.
    test_create_batch_4 should fail as create_batch() takes invalid PeriodicData request as input: 
        out of TimeLimit margins.
    """

    @mark.parametrize("time_limit, reference_batch",
                      (scenarios))
    def test_create_batch_1(self,
                            kaist_urban_dataset: Fixture,
                            sensor_factory: Fixture,
                            time_limit: TimeRange, reference_batch: DataBatch):

        cs = ConfigStore.instance()
        cs.store(name=BATCH_FACTORY_CONFIG_NAME, node=BFConfig)
        with initialize_config_module(config_module=CONFIG_MODULE_DIR):
            cfg = compose(config_name=BATCH_FACTORY_CONFIG_NAME)
            cfg.regime.start = time_limit.start
            cfg.regime.stop = time_limit.stop
            batch_factory = BatchFactory(cfg)

        batch_factory.create_batch()
        result_batch: DataBatch = batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if (isinstance(el1.measurement.values[0], Image) and
                    isinstance(el2.measurement.values[0], Image)):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2

    @mark.parametrize("time_limit, reference_batch",
                      (scenarios))
    def test_create_batch_2(self,
                            time_limit: TimeRange, reference_batch: DataBatch):
        cs = ConfigStore.instance()
        cs.store(name=BATCH_FACTORY_CONFIG_NAME, node=BFConfig)
        with initialize_config_module(config_module=CONFIG_MODULE_DIR):
            cfg = compose(config_name=BATCH_FACTORY_CONFIG_NAME)
            cfg.regime.start = time_limit.start
            cfg.regime.stop = time_limit.stop
            batch_factory = BatchFactory(cfg)

        elements: deque[Element] = reference_batch.data
        batch_factory.create_batch(elements)
        result_batch: DataBatch = batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if (isinstance(el1.measurement.values[0], Image) and
                    isinstance(el2.measurement.values[0], Image)):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2

    @mark.parametrize("time_limit, reference_batch, periodic_request",
                      (periodic_request_scenarios))
    def test_create_batch_3(self,
                            time_limit: TimeRange,
                            reference_batch: DataBatch,
                            periodic_request: set[PeriodicData]):
        cs = ConfigStore.instance()
        cs.store(name=BATCH_FACTORY_CONFIG_NAME, node=BFConfig)
        with initialize_config_module(config_module=CONFIG_MODULE_DIR):
            cfg = compose(config_name=BATCH_FACTORY_CONFIG_NAME)
            cfg.regime.start = time_limit.start
            cfg.regime.stop = time_limit.stop
            batch_factory = BatchFactory(cfg)

        batch_factory.create_batch(periodic_request)
        result_batch: DataBatch = batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if (isinstance(el1.measurement.values[0], Image) and
                    isinstance(el2.measurement.values[0], Image)):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2

    @mark.xfail
    @mark.parametrize("time_limit, reference_batch, periodic_request",
                      (incorrect_scenario))
    def test_create_batch_4(self,
                            time_limit: TimeRange,
                            reference_batch: DataBatch,
                            periodic_request: set[PeriodicData]):
        cs = ConfigStore.instance()
        cs.store(name=BATCH_FACTORY_CONFIG_NAME, node=BFConfig)
        with initialize_config_module(config_module=CONFIG_MODULE_DIR):
            cfg = compose(config_name=BATCH_FACTORY_CONFIG_NAME)
            cfg.regime.start = time_limit.start
            cfg.regime.stop = time_limit.stop
            batch_factory = BatchFactory(cfg)

        batch_factory.create_batch(periodic_request)
        result_batch: DataBatch = batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if (isinstance(el1.measurement.values[0], Image) and
                    isinstance(el2.measurement.values[0], Image)):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2
