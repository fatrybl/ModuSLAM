import logging
from collections import deque

from moduslam.data_manager.batch_factory.data_objects import Element
from moduslam.logger.logging_config import data_manager
from moduslam.utils.deque_set import DequeSet

logger = logging.getLogger(data_manager)


class DataBatch:
    """DataBatch is a container for data."""

    def __init__(self):
        self._deque_set = DequeSet[Element]()

    @property
    def data(self) -> deque[Element]:
        """Elements in the data batch."""
        return self._deque_set.items

    @property
    def empty(self) -> bool:
        """Data batch emptiness status."""
        return self._deque_set.empty

    @property
    def first(self) -> Element:
        """The first element of the batch."""
        return self._deque_set[0]

    @property
    def last(self) -> Element:
        """The first element of the batch."""
        return self._deque_set[-1]

    @property
    def size_bytes(self) -> int:
        """The size of the batch in bytes.

        Not implemented.
        """
        raise NotImplementedError

    @property
    def is_sorted(self) -> bool:
        """Order of the batch.

        Takes O(N) operations.
        """
        iterator = iter(self._deque_set.items)
        try:
            previous = next(iterator)
        except StopIteration:
            return True

        for current in iterator:
            if current.timestamp < previous.timestamp:
                return False
            previous = current

        return True

    def add(self, new_element: Element) -> None:
        """Adds new element to the Batch.

        Args:
            new_element: element to be added.
        """
        self._deque_set.append(new_element)

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

    def clear(self) -> None:
        """Deletes all elements of the batch."""
        self._deque_set.clear()
