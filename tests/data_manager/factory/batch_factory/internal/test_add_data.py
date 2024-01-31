"""
each sensor request:
    1) start==stop: start of dataset
    2) start==stop: end of dataset
    3) start==stop: middle of dataset
    4) start!=stop: all elements in dataset
    5) start!=stop: some middle elements in dataset
    6) start!=stop: from start to middle of dataset
    7) start!=stop: from middle to end of dataset
    8) start!=stop: from start to pre-end of dataset
    9) start!=stop: from 2nd-start to end of dataset

    In total: 9*N cases, 9 - number of test cases per sensor, N - number of sensors.
"""

from pytest import mark

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.batch_factory import BatchFactory
from slam.utils.auxiliary_dataclasses import PeriodicData
from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory
from tests.data_manager.factory.batch_factory.internal.data import (
    encoder_scenarios,
    lidar2D_scenarios,
    stereo_scenarios,
)


class TestBatchFactoryKaistDataset:
    @mark.parametrize("scenario", (encoder_scenarios))
    def test_add_data_csv(
        self,
        batch_factory: BatchFactory,
        scenario: tuple[PeriodicData, DataBatch],
    ):
        request: PeriodicData = scenario[0]
        reference_batch: DataBatch = scenario[1]
        batch_factory._add_data(request)
        assert batch_factory.batch.data == reference_batch.data

    @mark.parametrize("scenario", (lidar2D_scenarios))
    def test_add_data_bin(
        self,
        batch_factory: BatchFactory,
        scenario: tuple[PeriodicData, DataBatch],
    ):
        request: PeriodicData = scenario[0]
        reference_batch: DataBatch = scenario[1]
        batch_factory._add_data(request)
        assert batch_factory.batch.data == reference_batch.data

    @mark.parametrize("scenario", (stereo_scenarios))
    def test_add_data_imgs(
        self,
        batch_factory: BatchFactory,
        scenario: tuple[PeriodicData, DataBatch],
    ):
        request: PeriodicData = scenario[0]
        reference_batch: DataBatch = scenario[1]

        batch_factory._add_data(request)

        assert len(batch_factory.batch.data) == len(reference_batch.data)
        for el1, el2 in zip(batch_factory.batch.data, reference_batch.data):
            assert DataFactory.equal_images(el1, el2) is True
