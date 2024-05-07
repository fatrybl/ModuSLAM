class IndexStorage:
    """Storage of unique indices.

    If the storage is empty, min_idx = float(+inf) and max_idx = float(-inf)
    """

    def __init__(self):
        self._min_idx: int | float = float("inf")
        self._max_idx: int | float = float("-inf")
        self._indices: set[int] = set()

    @property
    def num_indices(self) -> int:
        """Number of indices in the storage."""
        return len(self._indices) if self._indices else 0

    @property
    def min_idx(self) -> int:
        """Minimum index in the storage."""
        return int(self._min_idx) if self._indices else 0

    @property
    def max_idx(self) -> int:
        """Maximum index in the storage."""
        return int(self._max_idx) if self._indices else 0

    @property
    def indices(self) -> set[int]:
        """Indices in the storage."""
        return self._indices

    def add(self, index: int) -> None:
        """Adds index to the storage.

        Args:
            index: index to add.
        """
        assert index >= 0, "index must be non-negative"
        self._indices.add(index)
        self._update_min_max(index)

    def remove(self, index: int) -> None:
        """Removes index from the storage.

        Args:
            index: index to remove.
        """
        assert index >= 0, "index must be non-negative"
        if index in self._indices:
            self._indices.remove(index)
            if self._indices:
                if index == self._min_idx:
                    self._min_idx = min(self._indices)
                if index == self._max_idx:
                    self._max_idx = max(self._indices)

            else:
                self._min_idx = float("inf")
                self._max_idx = float("-inf")
        else:
            raise KeyError(f"Index {index} has not been found in the storage.")

    def normalize(self) -> None:
        """Normalize indices to start from 0."""
        if self.min_idx == 0:
            return
        self._indices = {idx - self.min_idx for idx in self._indices}
        self._max_idx -= self.min_idx
        self._min_idx = 0

    def _update_min_max(self, index: int) -> None:
        """Updates min and max indices.

        Args:
            index: new index to update min and max indices.
        """
        self._min_idx = index if index < self._min_idx else self._min_idx
        self._max_idx = index if index > self._max_idx else self._max_idx


def generate_index(index_storage: IndexStorage) -> int:
    """
    Generates new index for the given indices with the rule:
        new index = max index + 1.

    Args:
        index_storage: storage of indices.

    Returns:
        new index.
    """
    return index_storage.max_idx + 1
