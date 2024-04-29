import logging
from collections import deque

from slam.data_manager.factory.element import Element
from slam.utils.deque_set import DequeSet

logger = logging.getLogger(__name__)


class DataBatch:
    """DataBatch is a container for data."""

    def __init__(self):
        self._deque_set = DequeSet[Element]()

    @property
    def data(self) -> deque[Element]:
        """Elements in the data batch."""
        return self._deque_set.items

    @property
    def first(self) -> Element:
        """The first element of the batch."""
        return self._deque_set[0]

    @property
    def size_bytes(self) -> int:
        """The size of the batch in bytes.\n Not implemented."""
        raise NotImplementedError

    def add(self, new_element: Element) -> None:
        """Adds new element to the Batch.

        Args:
            new_element: element to be added.
        """
        self._deque_set.add(new_element)

    def remove_first(self) -> None:
        """Deletes the first(left) element of the batch."""
        self._deque_set.remove_first()

    def remove_last(self) -> None:
        """Deletes the last(right) element of the batch."""
        self._deque_set.remove_last()

    def sort(self, reverse: bool = False) -> None:
        """Sorts the data batch by timestamps.

        Args:
            reverse: if True, sorts in descending order.
        """
        self._deque_set.sort(key=lambda element: element.timestamp, reverse=reverse)

    def empty(self) -> bool:
        """Checks if the batch is empty."""
        return self._deque_set.empty

    def clear(self) -> None:
        """Deletes all elements of the batch."""
        self._deque_set.clear()
