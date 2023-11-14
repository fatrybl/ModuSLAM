from collections import deque
from pytest import mark

from PIL.Image import Image

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.auxiliary_dataclasses import PeriodicData

from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory

from tests.data_manager.factory.batch_factory.conftest import Fixture
from .data import elements_batch, kaist_dataset_deque_scenario, kaist_dataset_requests_scenarios


class TestBatchFactoryKaistDataset:
    """
    Tests create_batch() method of a BatchFactory with Kaist Urban based dataset.

    Args: 
        kaist_batch_factory (BatchFactory): BatchFactory for particular Kaist Urban Dataset.
        scenario (tuple[set[PeriodicData], DataBatch]):test scenario: set of PeriodicData requests and 
            resulting DataBatch.
    """

    def test_create_batch_1(self, sensor_factory: Fixture, kaist_batch_factory: BatchFactory):
        reference_batch: DataBatch = elements_batch

        kaist_batch_factory.create_batch()
        result_batch: DataBatch = kaist_batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if (isinstance(el1.measurement.values[0], Image) and
                    isinstance(el2.measurement.values[0], Image)):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2

    def test_create_batch_2(self, kaist_batch_factory: BatchFactory):
        elements: deque[Element] = kaist_dataset_deque_scenario[0]
        reference_batch: DataBatch = kaist_dataset_deque_scenario[1]

        kaist_batch_factory.create_batch(elements)
        result_batch: DataBatch = kaist_batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if (isinstance(el1.measurement.values[0], Image) and
                    isinstance(el2.measurement.values[0], Image)):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2

    @mark.parametrize("scenario",
                      (kaist_dataset_requests_scenarios))
    def test_create_batch_3(self,
                            kaist_batch_factory: BatchFactory,
                            scenario: tuple[set[PeriodicData], DataBatch]):

        requests: set[PeriodicData] = scenario[0]
        reference_batch: DataBatch = scenario[1]
        reference_batch.sort()

        kaist_batch_factory.create_batch(requests)
        result_batch: DataBatch = kaist_batch_factory.batch

        assert len(result_batch.data) == len(reference_batch.data)

        for el1, el2 in zip(result_batch.data, reference_batch.data):
            if (isinstance(el1.measurement.values[0], Image) and
                    isinstance(el2.measurement.values[0], Image)):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2
