from phd.moduslam.frontend_manager.main_graph.graph import GraphCandidate
from phd.moduslam.utils.exceptions import ItemNotExistsError


class MetricsStorage:
    """Stores metrics for graph candidates."""

    _timeshift_table: dict[GraphCandidate, int] = {}
    _error_table: dict[GraphCandidate, float] = {}
    _connectivity_table: dict[GraphCandidate, bool] = {}

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
    def get_error_table(cls) -> dict[GraphCandidate, float]:
        """Gets the table with candidates and errors.

        Returns:
            the table with candidates and errors.
        """
        return cls._error_table

    @classmethod
    def get_timeshift_table(cls) -> dict[GraphCandidate, int]:
        """Gets the table with candidates and errors.

        Returns:
            the table with candidates and errors.
        """
        return cls._timeshift_table

    @classmethod
    def get_connectivity_status(cls, candidate: GraphCandidate) -> bool:
        """Returns connectivity status for the given candidate.

        Args:
            candidate: a graph candidate to get the status for.

        Returns:
            connectivity status.

        Raises:
            ItemNotExistsError: if no connectivity status exists for the given candidate.
        """
        try:
            return cls._connectivity_table[candidate]
        except KeyError:
            raise ItemNotExistsError("No connectivity status exists for the candidate.")

    @classmethod
    def clear(cls) -> None:
        """Clears all metrics from the storage."""
        cls._timeshift_table.clear()
        cls._error_table.clear()
        cls._connectivity_table.clear()
