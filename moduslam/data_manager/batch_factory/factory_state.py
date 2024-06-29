"""Manages current state of Batch Factory."""


class StoppingCriterion:
    def __init__(self):
        self._memory_limit_reached: bool = False
        self._is_data_processed: bool = False

    @property
    def active(self) -> bool:
        """Checks if any of stopping criteria is active."""
        return any((self._memory_limit_reached, self._is_data_processed))

    @property
    def memory_limit(self) -> bool:
        """Memory limit status."""
        return self._memory_limit_reached

    @memory_limit.setter
    def memory_limit(self, value: bool):
        self._memory_limit_reached = value

    @property
    def data_processed(self) -> bool:
        """All data processed status."""
        return self._is_data_processed

    @data_processed.setter
    def data_processed(self, value: bool):
        self._is_data_processed = value

    def reset(self):
        """Resets all state components to default values."""
        self._memory_limit_reached = False
        self._is_data_processed = False
