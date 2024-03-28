class IndexStorage:
    """Storage of unique indices."""

    def __init__(self):
        self.min_idx: int = 0
        self.max_idx: int = 0
        self.indices: set[int] = set()
        self.num_indices: int = 0

    def add(self, index: int):
        assert index >= 0, "index must be non-negative"
        self.indices.add(index)
        self.min_idx = index if index < self.min_idx else self.min_idx
        self.max_idx = index if index > self.max_idx else self.max_idx

    def remove(self, index: int):
        assert index >= 0, "index must be non-negative"
        self.indices.remove(index)
        if index == self.min_idx:
            self.min_idx = min(self.indices)
        if index == self.max_idx:
            self.max_idx = max(self.indices)

    def normalize(self):
        """Normalize indices to start from 0."""
        if self.min_idx == 0:
            return
        self.indices = {idx - self.min_idx for idx in self.indices}
        self.max_idx -= self.min_idx
        self.min_idx = 0


def generate_index(index_storage: IndexStorage):
    """
    Generates a new index based on the given indices:
    new index = max index + 1.

    Args:
        index_storage (IndexStorage): storage of indices.

    Returns:
        (int): new index.
    """
    return index_storage.max_idx + 1
