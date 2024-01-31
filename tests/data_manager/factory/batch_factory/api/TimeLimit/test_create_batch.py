from collections import deque

from PIL.Image import Image
from pytest import mark

from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig
from configs.system.data_manager.batch_factory.regime import TimeLimitConfig
from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.auxiliary_dataclasses import PeriodicData, TimeRange
from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory
from tests.data_manager.factory.batch_factory.api.TimeLimit.data import (
    incorrect_scenario,
    periodic_request_scenarios,
    scenarios,
)


class TestBatchFactoryKaistDataset:
    """
    Tests create_batch() method of a BatchFactory with Kaist Urban based dataset and "TimeLimit" regime.
    test_create_batch_4 should fail as create_batch() takes invalid PeriodicData request as input:
        out of TimeLimit margins.
    """

    @mark.parametrize("time_limit, reference_batch", (scenarios))
    def test_create_batch_1(
        self,
        batch_factory_cfg: BatchFactoryConfig,
        time_limit: TimeRange,
        reference_batch: DataBatch,
    ):
        regime_cfg: TimeLimitConfig = TimeLimitConfig(start=time_limit.start, stop=time_limit.stop)
        batch_factory_cfg.regime = regime_cfg
        batch_factory = BatchFactory(batch_factory_cfg)
        batch_factory.create_batch()
        result_batch: DataBatch = batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if isinstance(el1.measurement.values[0], Image) and isinstance(el2.measurement.values[0], Image):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2

    @mark.parametrize("time_limit, reference_batch", (scenarios))
    def test_create_batch_2(
        self,
        batch_factory_cfg: BatchFactoryConfig,
        time_limit: TimeRange,
        reference_batch: DataBatch,
    ):
        regime_cfg: TimeLimitConfig = TimeLimitConfig(start=time_limit.start, stop=time_limit.stop)
        batch_factory_cfg.regime = regime_cfg
        batch_factory = BatchFactory(batch_factory_cfg)

        elements: deque[Element] = reference_batch.data

        batch_factory.create_batch(elements)
        result_batch: DataBatch = batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if isinstance(el1.measurement.values[0], Image) and isinstance(el2.measurement.values[0], Image):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2

    @mark.parametrize("time_limit, reference_batch, periodic_request", (periodic_request_scenarios))
    def test_create_batch_3(
        self,
        batch_factory_cfg: BatchFactoryConfig,
        time_limit: TimeRange,
        reference_batch: DataBatch,
        periodic_request: set[PeriodicData],
    ):
        regime_cfg: TimeLimitConfig = TimeLimitConfig(start=time_limit.start, stop=time_limit.stop)
        batch_factory_cfg.regime = regime_cfg
        batch_factory = BatchFactory(batch_factory_cfg)

        batch_factory.create_batch(periodic_request)
        result_batch: DataBatch = batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if isinstance(el1.measurement.values[0], Image) and isinstance(el2.measurement.values[0], Image):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2

    @mark.xfail
    @mark.parametrize("time_limit, reference_batch, periodic_request", (incorrect_scenario))
    def test_create_batch_4(
        self,
        batch_factory_cfg: BatchFactoryConfig,
        time_limit: TimeRange,
        reference_batch: DataBatch,
        periodic_request: set[PeriodicData],
    ):
        regime_cfg: TimeLimitConfig = TimeLimitConfig(start=time_limit.start, stop=time_limit.stop)
        batch_factory_cfg.regime = regime_cfg
        batch_factory = BatchFactory(batch_factory_cfg)

        batch_factory.create_batch(periodic_request)
        result_batch: DataBatch = batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if isinstance(el1.measurement.values[0], Image) and isinstance(el2.measurement.values[0], Image):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2
