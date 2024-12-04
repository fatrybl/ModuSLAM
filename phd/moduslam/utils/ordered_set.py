"""Ordered-set data structure implementation."""

from collections import OrderedDict
from collections.abc import Iterable, Iterator, MutableSet, Sequence
from typing import Any, Generic, TypeVar, overload

T = TypeVar("T")


class OrderedSet(MutableSet, Sequence, Generic[T]):
    """OrderedSet is a combination of set and OrderedDict.

    Complexity:
    O(1): add, discard, remove, remove_first, remove_last, contains, first, last
    O(N): __getitem__(index), insert(item, index)
    """

    def __init__(self):
        self._items: OrderedDict[T, None] = OrderedDict()

    def __contains__(self, item: object) -> bool:
        return item in self._items

    def __iter__(self) -> Iterator[T]:
        return iter(self._items.keys())

    def __len__(self) -> int:
        return len(self._items.keys())

    def __repr__(self) -> str:
        return f"OrderedSet with {len(self._items)} items)"

    def __bool__(self) -> bool:
        return len(self) > 0

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]: ...

    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        """Complexity: O(N)

        Args:
            index: index of an item or a slice.

        Returns:
            item or a sequence of items.

        Raises:
            IndexError: if index is out of range.
        """
        if isinstance(index, slice):
            return [list(self._items.keys())[i] for i in range(*index.indices(len(self._items)))]

        elif isinstance(index, int):
            try:
                return list(self._items.keys())[index]

            except IndexError:
                raise IndexError("OrderedSet index out of range")
        else:
            raise TypeError("Invalid argument type.")

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
            item: item(s) to be added.

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

    def insert(self, item: T, index: int) -> None:
        """Inserts new item to the given position.
        Complexity: O(N).

        Args:
            item: an item to be inserted.

            index: index at which to insert the item.

        TODO: add tests.
        """
        items_list = list(self._items)
        items_list.insert(index, item)
        self._items.clear()
        for item in items_list:
            self.add(item)

    def discard(self, item: T | Iterable[T]) -> None:
        """Removes an item from the OrderedSet if it is present.

        Args:
            item: item(s) to be removed.
        """

        if isinstance(item, Iterable):
            for i in item:
                if i in self._items:
                    self._items.pop(i)
        else:
            if item in self._items:
                self._items.pop(item)

    def remove(self, item: T | Iterable[T]) -> None:
        """Removes an item from the OrderedSet if it is present.

        Args:
            item: item(s) to be removed.

        Raises:
            KeyError: if an item is not present in the OrderedSet.
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
