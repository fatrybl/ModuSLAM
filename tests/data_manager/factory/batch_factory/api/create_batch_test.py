from pytest import mark
from slam.data_manager.factory.batch import DataBatch

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.utils.auxiliary_dataclasses import PeriodicData

from .data import kaist_dataset_scenarios

"""
each sensor request:
    1) start==stop: start of dataset
    2) start==stop: end of dataset
    3) start==stop: middle of dataset
    4) start!=stop: from start to stop: all elements in dataset
    5) start!=stop: from start to stop: in the middle of the dataset
    6) start!=stop: from start to stop: start to middle of the dataset
    7) start!=stop: from start to stop: middle to stop of the dataset

    In total: 7*N cases, 7 - number of test cases per sensor, N - number of sensors.
"""


# def is_equal(deq1: deque, deq2: deque) -> bool:
#     assert len(deq1) == len(deq2)
#     for d1, d2 in zip(deq1, deq2):
#         if d1 != d2:
#             return False
#     return True

class TestBatchFactoryKaistDataset:

    @mark.parametrize("scenario",
                      (kaist_dataset_scenarios))
    def test_create_batch(self,
                          kaist_batch_factory: BatchFactory,
                          scenario: tuple[set[PeriodicData], DataBatch]):
        requests: set[PeriodicData] = scenario[0]
        reference_batch: DataBatch = scenario[1]
        kaist_batch_factory.create_batch(requests)
        assert kaist_batch_factory.batch.data == reference_batch.data
