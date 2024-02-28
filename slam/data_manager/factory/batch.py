import logging
from collections import deque

from slam.data_manager.factory.element import Element
from slam.utils.deque_set import DequeSet

logger = logging.getLogger(__name__)


class DataBatch:
    """DataBatch is a container for data.

    TODO: integrate this class into DataManager->Batch
    """

    def __init__(self):
        self._deque_set = DequeSet[Element]()

    def add(self, new_element: Element) -> None:
        """Adds new element to the Batch. 1) Add to set[Element] to avoid duplicates. 2)
        Add to deque for fast front-pop().

        Args:
            new_element (Element): element to be added.
        """
        self._deque_set.add(new_element)

    def delete_first(self) -> None:
        """Deletes the first(left) element of the batch."""
        self._deque_set.remove_first()

    def delete_last(self) -> None:
        """Deletes the last(right) element of the batch."""
        self._deque_set.remove_last()

    def sort(self, reverse: bool = False) -> None:
        """Sorts the data batch by timestamp.

        Args:
            reverse (bool): if True, sorts in descending order.
        """
        self._deque_set.sort(key=lambda element: element.timestamp, reverse=reverse)

    def empty(self) -> bool:
        """Checks if the batch is empty."""
        return self._deque_set.is_empty()

    def clear(self) -> None:
        """Deletes all elements of the batch."""
        self._deque_set.clear()

    @property
    def data(self) -> deque[Element]:
        """Elements in the data batch.

        Returns:
            deque[Element]: elements in the batch.
        """
        return self._deque_set.items

    @property
    def first_element(self):
        """Returns the first element of the batch.

        Returns:
            element (Element): first element of the batch.
        """
        return self.data[0]

    @property
    def size_bytes(self) -> int:
        """Returns the size of the batch in bytes.

        Returns:
            size (int): size of the batch in bytes.
        """
        raise NotImplementedError
