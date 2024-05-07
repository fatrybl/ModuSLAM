"""Ordered-set data structure implementation.

Complexity:
    O(1): add(), contains(item: T), remove(item), remove_first, remove_last.
    O(N): __getitem__(index: int).
"""

from collections import OrderedDict
from typing import Any, Generic, Iterable, TypeVar

T = TypeVar("T")


class OrderedSet(Generic[T]):
    """OrderedSet is a combination of set and OrderedDict."""

    def __init__(self, iterable: Iterable[T] | None = None):
        self._items: OrderedDict[T, None] = OrderedDict()

        if iterable:
            for item in iterable:
                self.add(item)

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def __iter__(self):
        return iter(self._items.keys())

    def __len__(self) -> int:
        return len(self._items.keys())

    def __repr__(self) -> str:
        return f"OrderedSet({set(self._items.keys())})"

    def __getitem__(self, index: int) -> T:
        """
        Attention: This method requires O(n) time complexity.

        Args:
            index: index of an item.

        Returns:
            item.

        Raises:
            IndexError: if index is out of range.
        """
        try:
            return list(self._items.keys())[index]

        except IndexError:
            raise IndexError("OrderedSet index out of range")

    def __eq__(self, other: Any) -> bool:
        """Compares if an OrderedSet is equal to another OrderedSet. Two OrderedSets are
        equal if they have the same elements in the same order.

        Args:
            other: OrderedSet to compare with.

        Returns:
            equality status.
        """
        if isinstance(other, OrderedSet):
            return self._items == other._items
        return False

    @property
    def items(self):
        """All items in OrderedSet."""
        return self._items.keys()

    @property
    def first(self) -> T:
        """First item in OrderedSet.

        Raises:
            KeyError: if OrderedSet is empty.
        """
        if len(self._items) == 0:
            raise KeyError("OrderedSet is empty")
        return next(iter(self._items))

    @property
    def last(self) -> T:
        """Last item in OrderedSet.

        Raises:
            KeyError: if OrderedSet is empty.
        """
        if len(self._items) == 0:
            raise KeyError("OrderedSet is empty")
        return next(reversed(self._items))

    def add(self, item: T | Iterable[T]) -> None:
        """Adds an item to the OrderedSet.

        Args:
            item (T): item(s) to be added.

        Raises:
            TypeError: if an item is not hashable.
        """
        msg = "Item is not hashable and cannot be used as a key in the OrderedDict."

        if isinstance(item, Iterable):
            for i in item:
                if self._is_hashable(i):
                    self._items[i] = None
                else:
                    raise TypeError(msg)

        else:
            if self._is_hashable(item):
                self._items[item] = None
            else:
                raise TypeError(msg)

    def remove(self, item: T | Iterable[T]) -> None:
        """Removes an item or items from the OrderedSet.

        Args:
            item: item(s) to be removed.

        Raises:
            KeyError: if an item is not in the OrderedSet.
        """
        msg = "Item not found in OrderedSet:"

        if isinstance(item, Iterable):
            for i in item:
                if i in self._items:
                    self._items.pop(i)
                else:
                    raise KeyError(msg + f" {i}")
        else:
            if item in self._items:
                self._items.pop(item)
            else:
                raise KeyError(msg + f" {item}")

    @staticmethod
    def _is_hashable(item: T) -> bool:
        """Checks if an item is hashable.

        Args:
            item: item to check.

        Returns:
            hash ability status.
        """
        try:
            hash(item)
            return True
        except TypeError:
            return False
