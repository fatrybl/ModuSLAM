# from typing import Type
# from pytest import mark
# from unittest.mock import patch

# from slam.data_manager.factory.batch import DataBatch
# from slam.data_manager.factory.batch_factory import BatchFactory
# from slam.data_manager.factory.readers.element_factory import Element
# from slam.utils.auxiliary_dataclasses import PeriodicData

# from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig

# from .data import data_batch

# """
# Tests description:

# 1) Genereate dataset.
# 2) Create reference Data Batch.
# 3) Create Data Batch with by request.
# 4) Compare reference Data Batch with resulting Data Batch.

# Test cases:
#     1 request:
#         1) 1 sensor, start==stop: start of dataset
#         2) 1 sensor, start==stop: end of dataset
#         3) 1 sensor, start==stop: middle of dataset
#         4) 1 sensor, start!=stop: from start to stop: all elements in dataset
#         5) 1 sensor, start!=stop: from start to stop: in the middle of the dataset
#         6) 1 sensor, start!=stop: from start to stop: from start to middle of the dataset
#         7) 1 sensor, start!=stop: from start to stop: from middle to stop of the dataset
# """


# OBJECT_PATH_TO_PATCH = "slam.data_manager.factory.readers.kaist.kaist_reader.SensorFactory"


# class AddData:

#     batch: DataBatch = DataBatch()

#     @mark.parametrize("reference_data_batch, request",
#                       ([data_batch, request]))
#     @patch(OBJECT_PATH_TO_PATCH)
#     def _add_data(self, batch_factory: BatchFactory, reference_data_batch: DataBatch, request: PeriodicData) -> None:

#         batch_factory._add_data(request)
#         batch = batch_factory.batch
#         # assert self.batch.data == batch_factory.batch.data
#         assert 1 == 1
