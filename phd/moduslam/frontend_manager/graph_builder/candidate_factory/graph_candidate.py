import logging
from collections import deque

from moduslam.frontend_manager.measurement_storage import MeasurementStorage
from moduslam.logger.logging_config import frontend_manager
from moduslam.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(frontend_manager)


class State(MeasurementStorage):
    """State of the storage with measurements in exact time moment.

    Used for the graph candidate.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def timestamp(self) -> int:
        """Time stamp of the state."""
        return self.time_range.stop


class GraphCandidate:
    """Graph candidate.

    Contains a sequence of states and the time range of the graph candidate.
    """

    def __init__(self) -> None:
        self._states: deque[State] = deque()
        self._time_range: TimeRange | None = None

    @property
    def time_range(self) -> TimeRange:
        """Time range of the graph candidate."""

        self._time_range = self._update_time_range()
        return self._time_range

    @property
    def states(self) -> deque[State]:
        """States of the graph candidate."""

        return self._states

    def add(self, state: State) -> None:
        """Adds a state to the graph candidate."""

        self.states.append(state)

    def remove(self, state: State) -> None:
        """Removes the state from the graph candidate."""

        self.states.remove(state)

    def remove_first(self) -> None:
        """Removes the first state from the graph candidate."""

        self.states.popleft()

    def remove_last(self) -> None:
        """Removes the last state from the graph candidate."""

        self.states.pop()

    def clear(self) -> None:
        """Clears the graph candidate."""

        self._states = deque()
        self._time_range = None

    def _update_time_range(self) -> TimeRange:
        """Updates the time range of the graph candidate.

        Returns:
            time range of the graph candidate.

        Raises:
            ValueError: if the graph candidate is empty.
        """

        if not self.states:
            msg = "Empty graph candidate."
            logger.critical(msg)
            raise ValueError(msg)

        start = min(s.time_range.start for s in self.states)
        stop = max(s.time_range.stop for s in self.states)
        return TimeRange(start, stop)
