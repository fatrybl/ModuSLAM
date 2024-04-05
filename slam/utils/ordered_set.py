"""Custom ordered-set implementation.

Complexity:
    O(1): add(), contains(item: T), remove(item: T), first, last.
    O(N): __getitem__(index: int).
"""

from collections import OrderedDict
from typing import Any, Generic, Iterable, TypeVar, overload

from plum import dispatch

T = TypeVar("T")


class OrderedSet(Generic[T]):
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

    @staticmethod
    def _is_hashable(item: T) -> bool:
        try:
            hash(item)
            return True
        except TypeError:
            return False

    def __repr__(self) -> str:
        return f"OrderedSet({set(self._items.keys())})"

    def __getitem__(self, index: int) -> T:
        """
        Attention: This method requires O(n) time complexity.

        Args:
            index (int): index of the item.

        Returns:
            (T): item at the given index.
        """
        try:
            return list(self._items.keys())[index]
        except IndexError:
            raise IndexError("OrderedSet index out of range")

    def __eq__(self, other: Any) -> bool:
        """Compares if this OrderedSet is equal to another OrderedSet. Two OrderedSets
        are equal if they have the same elements in the same order.

        Args:
            other (Any): The other OrderedSet to compare with.

        Returns:
            bool: True if the two OrderedSets are equal, False otherwise.
        """
        if isinstance(other, OrderedSet):
            return self._items == other._items
        return False

    @property
    def items(self):
        return self._items.keys()

    @property
    def first(self) -> T:
        if len(self._items) == 0:
            raise KeyError("OrderedSet is empty")
        return next(iter(self._items))

    @property
    def last(self) -> T:
        if len(self._items) == 0:
            raise KeyError("OrderedSet is empty")
        return next(reversed(self._items))

    @overload
    def add(self, items: Iterable[T]) -> None:
        """Adds items from the given iterable.

        Args:
            items (Iterable[T]): items to be added.
        """
        for item in items:
            self.add(item)

    @overload
    def add(self, item: T) -> None:
        if self._is_hashable(item):
            self._items[item] = None
        else:
            raise TypeError("Item is not hashable and cannot be used as a key in the OrderedDict.")

    @dispatch
    def add(self, item=None):
        """
        Calls:
            1.  add single item.
                Args:
                    item (T): item to be added.

            2.  add multiple items.
                Args:
                    items (Iterable[T]): items to be added.
        """

    def remove(self, item: T) -> None:
        self._items.pop(item, None)
