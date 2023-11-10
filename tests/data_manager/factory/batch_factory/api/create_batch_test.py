from pytest import mark

from PIL.Image import Image

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.batch_factory import BatchFactory
from slam.utils.auxiliary_dataclasses import PeriodicData
from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory

from .data import kaist_dataset_scenarios


class TestBatchFactoryKaistDataset:
    """
    Tests create_batch() method of a BatchFactory with Kaist Urban based dataset.

    Args: 
        <ANY>_batch_factory (BatchFactory): any BatchFactory for particular dataset.
        scenario (tuple[set[PeriodicData], DataBatch]):test scenario: set of PeriodicData requests and 
            resulting DataBatch.
    """

    @mark.parametrize("scenario",
                      (kaist_dataset_scenarios))
    def test_create_batch(self,
                          kaist_batch_factory: BatchFactory,
                          scenario: tuple[set[PeriodicData], DataBatch]):

        requests: set[PeriodicData] = scenario[0]
        reference_batch: DataBatch = scenario[1]

        kaist_batch_factory.create_batch(requests)

        reference_batch.sort()
        kaist_batch_factory.batch.sort()

        assert len(kaist_batch_factory.batch.data) == len(reference_batch.data)

        for el1, el2 in zip(kaist_batch_factory.batch.data, reference_batch.data):
            if (isinstance(el1.measurement.values[0], Image) and
                    isinstance(el2.measurement.values[0], Image)):
                assert DataFactory.equal_images(el1, el2) is True
            else:
                assert el1 == el2
