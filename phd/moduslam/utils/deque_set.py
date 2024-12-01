"""Deque-set data structure implementation."""

from collections import deque
from collections.abc import Iterable, Sequence
from typing import Any, Callable, Generic, TypeVar, overload

T = TypeVar("T")


class DequeSet(Sequence, Generic[T]):
    """DequeSet is a combination of set and deque.

    Complexity:
    O(1): add, contains(item), remove_first, remove_last, __getitem__(index).
    O(N): remove(item)
    """

    def __init__(self):
        self._deque = deque[T]()
        self._set = set[T]()

    def __contains__(self, item) -> bool:
        return item in self._set

    def __len__(self) -> int:
        return len(self._set)

    def __iter__(self):
        return iter(self._deque)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]: ...

    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        """Complexity: O(K) for slice, O(1) for index access.

        Args:
            index: index of an item or a slice.

        Returns:
            item or a sequence of items.

        Raises:
            TypeError: invalid argument type.

        TODO: add tests
        """
        return self._deque[index]  # type: ignore

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

    def append(self, item: T | Iterable[T]) -> None:
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

    def insert(self, item: T, index: int):
        """Inserts new item to the given position.

        Args:
            item: an item to be inserted.

            index: index at which to insert the item.
        """
        if item not in self._set:
            self._set.add(item)
            self._deque.insert(index, item)

    def remove(self, item: T) -> None:
        """Removes item from set and deque.

        Args:
            item: item to be removed.
        """

        if isinstance(item, Iterable):
            for i in item:
                self._set.remove(i)
                self._deque.remove(i)

        else:
            self._set.remove(item)
            self._deque.remove(item)

    def remove_first(self) -> None:
        """Removes first item from deque-set."""
        item = self._deque.popleft()
        self._set.remove(item)

    def remove_last(self) -> None:
        """Removes last item from deque-set."""
        item = self._deque.pop()
        self._set.remove(item)

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
