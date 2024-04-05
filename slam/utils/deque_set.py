"""Custom deque-set implementation.

Complexity:
    O(1): add(), contains(item: T), remove_first(), remove_last(), __getitem__(index: int).
    O(N): remove(item: T)
"""

import functools
import logging
from collections import deque
from typing import Any, Callable, Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def multiple(func: Callable):
    """Decorator for multiple deque-sets.

    Args:
        func (Callable): function to be decorated.
    """

    @functools.wraps(func)
    def wrapper(self, item):
        func(self, item)
        for ds in self._deque_sets:
            getattr(ds, func.__name__)(item)

    return wrapper


class DequeSet(Generic[T]):
    """DequeSet is a combination of set and deque."""

    def __init__(self):
        self._deque: deque[T] = deque()
        self._set: set[T] = set()

    def __contains__(self, item) -> bool:
        return item in self._set

    def __len__(self) -> int:
        return len(self._set)

    def __iter__(self):
        return iter(self._deque)

    def __getitem__(self, item) -> T:
        return self._deque[item]

    def __eq__(self, other: Any) -> bool:
        """Compares if this DequeSet is equal to another DequeSet. Two DequeSets are
        equal if they have the same elements in the same order.

        Args:
            other (Any): The other DequeSet to compare with.

        Returns:
            bool: True if the two DequeSets are equal, False otherwise.
        """
        if isinstance(other, DequeSet):
            return self._deque == other._deque and self._set == other._set
        return False

    def add(self, item: T) -> None:
        """
        Adds new item:
            1) Add to set to avoid duplicates.
            2) Add to deque for fast front-pop().

        Args:
            item (Any): new item to be added.
        """
        if item not in self._set:
            self._set.add(item)
            self._deque.append(item)

    def remove(self, item: T) -> None:
        """Removes item from set and deque.

        Args:
            item (T): item to be removed.
        """
        try:
            self._set.remove(item)
            self._deque.remove(item)
        except KeyError:
            msg = f"No item {item} in set or deque"
            logger.error(msg)

    def remove_first(self) -> None:
        """Removes first item from set and deque."""
        try:
            item: T = self._deque.popleft()
            self._set.remove(item)
        except KeyError:
            msg = "Empty set or deque"
            logger.error(msg)

    def remove_last(self) -> None:
        """Removes last item from set and deque."""
        try:
            item: T = self._deque.pop()
            self._set.remove(item)
        except KeyError:
            msg = "Empty set or deque"
            logger.error(msg)

    def sort(self, key, reverse: bool = False) -> None:
        """Sorts deque with the given key.

        Args:
            key:
            reverse (bool):
        """
        self._deque = deque(sorted(self._deque, key=key, reverse=reverse))

    def is_empty(self) -> bool:
        """Checks if deque-set is empty."""
        return not (bool(self._set) and bool(self._deque))

    def clear(self) -> None:
        """Clears deque-set."""
        self._set.clear()
        self._deque.clear()

    @property
    def items(self) -> deque[T]:
        """Returns deque of elements.

        Returns:
            (deque[T]): deque of elements of type T.
        """
        return self._deque


class MultipleDequeSet(DequeSet):
    """Stores multiple deque-sets as one."""

    def __init__(self, *deque_sets: DequeSet) -> None:
        super().__init__()
        self._deque_sets = deque_sets

    @multiple
    def add(self, item: T) -> None:
        super().add(item)

    @multiple
    def remove(self, item: T) -> None:
        super().remove(item)
