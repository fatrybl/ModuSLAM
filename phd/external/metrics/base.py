from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Metrics(Protocol):
    """Protocol for all metrics."""

    @classmethod
    def compute(cls, *args, **kwargs) -> Any:
        """Computes metrics for the graph and the measurements.

        Returns:
            metrics value.
        """
