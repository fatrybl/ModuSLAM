from collections import deque

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.auxiliary_dataclasses import PeriodicData


class BatchFactoryTest:

    def create_batch_1(self):
        pass

    def create_batch_2(self, elements: deque[Element]):
        pass

    def create_batch_3(self, requests: set[PeriodicData]):
        pass
