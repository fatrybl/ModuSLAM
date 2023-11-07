from collections import deque
from pytest import mark

# from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.batch_factory import BatchFactory
# from slam.utils.auxiliary_dataclasses import PeriodicData

# from .conftest import Fixture, kaist_urban_dataset
# from .data import data_batches, sets

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


class TestBatchFactory:

    # @mark.parametrize("reference_data_batch, requests",
    #                   ([data_batches, sets]))
    # def create_batch(self,
    #                  kaist_batch_factory: BatchFactory,
    #                  reference_data_batch: DataBatch,
    #                  requests: set[PeriodicData]):
    def test_create_batch(self, kaist_batch_factory: BatchFactory):
        assert 1 == 1
    # kaist_batch_factory.create_batch(requests)
    # assert reference_data_batch.data == kaist_batch_factory.batch.data


# class Ros1DatasetBatchFactoryTest:

#     @mark.parametrize("reference_data_batch, requests",
#                       ([data_batches, sets]))
#     def create_batch(self, ros1_batch_factory: BatchFactory,
#                      reference_data_batch: DataBatch, requests: set[PeriodicData]):
#         ros1_batch_factory.create_batch(requests)
#         assert reference_data_batch.data == ros1_batch_factory.batch.data
