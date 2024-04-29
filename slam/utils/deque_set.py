"""Deque-set data structure implementation.

Complexity:
    O(1): add(), contains(item: T), remove_first(), remove_last(), __getitem__(index: int).
    O(N): remove(item: T)
"""

import functools
import logging
from collections import deque
from collections.abc import Iterable
from typing import Any, Callable, Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def multiple(func: Callable):
    """Decorator for multiple deque-sets.

    Args:
        func: function to be decorated.
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
            other: DequeSet to compare with.

        Returns:
            equality result.
        """
        if isinstance(other, DequeSet):
            return self._deque == other._deque and self._set == other._set

        return False

    @property
    def items(self) -> deque[T]:
        """Items in deque-set."""
        return self._deque

    @property
    def empty(self) -> bool:
        """Empty status of deque-set."""
        return not (bool(self._set) and bool(self._deque))

    def add(self, item: T | Iterable[T]) -> None:
        """
        Adds new item:
            1) Add to set to avoid duplicates.\n
            2) Add to deque for fast front-pop().

        Args:
            item: item(s) to be added.
        """
        if isinstance(item, Iterable):
            for i in item:
                if i not in self._set:
                    self._set.add(i)
                    self._deque.append(i)
        else:
            if item not in self._set:
                self._set.add(item)
                self._deque.append(item)

    def remove(self, item: T) -> None:
        """Removes item from set and deque.

        Args:
            item: item to be removed.

        Raises:
            KeyError: if item is not in deque-set.
        """
        msg = "Item is not present in deque-set:"

        if isinstance(item, Iterable):
            for i in item:
                try:
                    self._set.remove(i)
                    self._deque.remove(i)
                except KeyError:
                    logger.error(msg + f" {i}")
                    raise
        else:
            try:
                self._set.remove(item)
                self._deque.remove(item)
            except KeyError:
                logger.error(msg + f" {item}")
                raise

    def remove_first(self) -> None:
        """Removes first item from deque-set.

        Raises:
            KeyError: if deque is empty
        """
        try:
            item: T = self._deque.popleft()
            self._set.remove(item)
        except KeyError:
            logger.error("Empty deque-set")
            raise

    def remove_last(self) -> None:
        """Removes last item from deque-set.

        Raises:
            KeyError: if deque-set is empty
        """
        try:
            item: T = self._deque.pop()
            self._set.remove(item)
        except KeyError:
            logger.error("Empty deque-set")
            raise

    def sort(self, key: Callable, reverse: bool = False) -> None:
        """Sorts deque with the given key.

        Args:
            key: key function to sort deque.
            reverse: reverse sorting order.
        """
        self._deque = deque(sorted(self._deque, key=key, reverse=reverse))

    def clear(self) -> None:
        """Clears deque-set."""
        self._set.clear()
        self._deque.clear()


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
