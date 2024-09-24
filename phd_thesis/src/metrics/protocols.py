from typing import Protocol, runtime_checkable

from phd_thesis.src.objects import Graph


@runtime_checkable
class Metrics(Protocol):
    """Protocol for all metrics."""

    @classmethod
    def compute(cls, graph: Graph, *args, **kwargs):
        """Computes metrics for the graph and the measurements.

        Args:
            graph: graph to compute metrics for.

        Returns:
            metrics value.
        """
