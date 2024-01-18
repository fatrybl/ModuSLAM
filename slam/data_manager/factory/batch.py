import logging
from collections import deque

from slam.data_manager.factory.readers.element_factory import Element

logger = logging.getLogger(__name__)


class DataBatch:
    def __init__(self):
        self._deque: deque[Element] = deque()
        self._set: set[Element] = set()

    def add(self, new_element: Element) -> None:
        """
        Adds new element to the Batch.
        1) Add to set[Element] to avoid duplicates.
        2) Add to deque for fast front-pop().

        Args:
            new_element (Element): element to be added.
        """
        if new_element not in self._set:
            self._set.add(new_element)
            self._deque.append(new_element)
        else:
            msg = "Skipping duplicate element!"
            logger.info(msg)

    def delete_first(self) -> None:
        """
        Deletes the first(left) element of the batch.
        """
        el: Element = self._deque.popleft()
        self._set.remove(el)

    def delete_last(self) -> None:
        """
        Deletes the last(right) element of the batch.
        """
        el: Element = self._deque.pop()
        self._set.remove(el)

    def sort(self) -> None:
        self._deque = deque(sorted(self._deque, key=lambda element: element.timestamp))

    def empty(self) -> bool:
        """
        Checks if the batch is empty.
        """
        if len(self._set) == 0 and len(self._deque) == 0:
            return False
        else:
            return True

    def clear(self) -> None:
        """
        Deletes all elements of the batch.
        """
        self._set.clear()
        self._deque.clear()

    @property
    def data(self) -> deque[Element]:
        return self._deque

    @property
    def first_element(self):
        return self.data[0]

    @property
    def size_bytes(self) -> int:
        raise NotImplementedError
