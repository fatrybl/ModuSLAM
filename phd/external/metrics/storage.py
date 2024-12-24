from phd.moduslam.frontend_manager.main_graph.graph import GraphCandidate
from phd.utils.exceptions import ItemNotExistsError


class MetricsStorage:
    """Stores metrics for graph candidates."""

    _timeshift_table: dict[GraphCandidate, int] = {}
    _error_table: dict[GraphCandidate, float] = {}
    _connectivity_table: dict[GraphCandidate, bool] = {}
    _mom_table: dict[GraphCandidate, float] = {}

    @classmethod
    def add_mom(cls, candidate: GraphCandidate, value: float) -> None:
        """Adds MOM-metric value to the table."""
        cls._mom_table[candidate] = value

    @classmethod
    def add_connectivity(cls, candidate: GraphCandidate, value: bool) -> None:
        """Adds connectivity value to the table."""
        cls._connectivity_table[candidate] = value

    @classmethod
    def add_timeshift(cls, candidate: GraphCandidate, value: int) -> None:
        """Adds timeshift value to the table."""
        cls._timeshift_table[candidate] = value

    @classmethod
    def add_error(cls, candidate: GraphCandidate, value: float) -> None:
        """Adds error value to the table."""
        cls._error_table[candidate] = value

    @classmethod
    def get_mom_table(cls) -> dict[GraphCandidate, float]:
        """The table with candidates and MOM values."""
        return cls._mom_table

    @classmethod
    def get_error_table(cls) -> dict[GraphCandidate, float]:
        """The table with candidates and solver error values."""
        return cls._error_table

    @classmethod
    def get_timeshift_table(cls) -> dict[GraphCandidate, int]:
        """The table with candidates and accumulative time shifts."""
        return cls._timeshift_table

    @classmethod
    def get_connectivity_status(cls, candidate: GraphCandidate) -> bool:
        """The connectivity status of the candidate.

        Args:
            candidate: a candidate to get connectivity status for.

        Raises:
            ItemNotExistsError: if no connectivity status exists for the given candidate.
        """
        try:
            return cls._connectivity_table[candidate]
        except KeyError:
            raise ItemNotExistsError("No connectivity status exists for the candidate.")

    @classmethod
    def clear(cls) -> None:
        """Clears all metrics in the storage."""
        cls._timeshift_table.clear()
        cls._error_table.clear()
        cls._connectivity_table.clear()
        cls._mom_table.clear()
