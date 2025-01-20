from src.moduslam.frontend_manager.main_graph.graph import GraphCandidate
from src.utils.exceptions import ItemNotExistsError


class MetricsStorage:
    """Stores metrics for graph candidates."""

    def __init__(self):
        self._timeshift_table: dict[GraphCandidate, int] = {}
        self._error_table: dict[GraphCandidate, float] = {}
        self._connectivity_table: dict[GraphCandidate, bool] = {}
        self._mom_table: dict[GraphCandidate, float] = {}
        self._unused_measurements: dict[GraphCandidate, int] = {}

    def add_mom(self, candidate: GraphCandidate, value: float) -> None:
        """Adds MOM-metric value to the table."""
        self._mom_table[candidate] = value

    def add_connectivity(self, candidate: GraphCandidate, value: bool) -> None:
        """Adds connectivity value to the table."""
        self._connectivity_table[candidate] = value

    def add_timeshift(self, candidate: GraphCandidate, value: int) -> None:
        """Adds timeshift value to the table."""
        self._timeshift_table[candidate] = value

    def add_solver_error(self, candidate: GraphCandidate, value: float) -> None:
        """Adds solver error value to the table."""
        self._error_table[candidate] = value

    def add_unused_measurements(self, candidate: GraphCandidate, value: int) -> None:
        """Adds number of unused measurements to the table."""
        self._unused_measurements[candidate] = value

    def get_mom_table(self) -> dict[GraphCandidate, float]:
        """The table with candidates and MOM values."""
        return self._mom_table

    def get_error_table(self) -> dict[GraphCandidate, float]:
        """The table with candidates and solver error values."""
        return self._error_table

    def get_timeshift_table(self) -> dict[GraphCandidate, int]:
        """The table with candidates and accumulative time shifts."""
        return self._timeshift_table

    def get_unused_measurements_table(self) -> dict[GraphCandidate, int]:
        """The table with candidates and number of unused measurements."""
        return self._unused_measurements

    def get_connectivity_status(self, candidate: GraphCandidate) -> bool:
        """The connectivity status of the candidate.

        Args:
            candidate: a candidate to get connectivity status for.

        Raises:
            ItemNotExistsError: if no connectivity status exists for the given candidate.
        """
        try:
            return self._connectivity_table[candidate]
        except KeyError:
            raise ItemNotExistsError("No connectivity status exists for the candidate.")

    def clear(self) -> None:
        """Clears all metrics in the storage."""
        self._timeshift_table.clear()
        self._error_table.clear()
        self._connectivity_table.clear()
        self._mom_table.clear()
        self._unused_measurements.clear()
