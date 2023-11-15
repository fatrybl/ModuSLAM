import logging
from collections import deque

from slam.data_manager.factory.readers.element_factory import Element

logger = logging.getLogger(__name__)


class DataBatch:
    def __init__(self):
        self.__data_deque: deque[Element] = deque()
        self.__data_set: set[Element] = set()

    def add(self, new_element: Element) -> None:
        """
        Adds new element to the Batch.
        1) Add to set[Element] to avoid duplicates.
        2) Add to deque.

        Args:
            new_element (Element): element to be added.
        """
        if new_element not in self.__data_set:
            self.__data_set.add(new_element)
            self.__data_deque.append(new_element)
        else:
            msg = f"Skipping duplicate element!"
            logger.info(msg)

    def sort(self) -> None:
        self.__data_deque = deque(sorted(
            self.__data_deque,
            key=lambda element: element.timestamp))

    @property
    def data(self) -> deque[Element]:
        return self.__data_deque

    @data.deleter
    def data(self) -> None:
        self.__data_set.clear()
        self.__data_deque.clear()

    @property
    def size_bytes(self) -> int:
        raise NotImplementedError
