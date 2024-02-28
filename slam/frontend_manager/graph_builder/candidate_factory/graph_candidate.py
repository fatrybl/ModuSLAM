from collections import deque
from dataclasses import dataclass, field

from slam.frontend_manager.element_distributor.elements_distributor import (
    MeasurementStorage,
)


@dataclass
class State:
    """State of the graph candidate."""

    storage: MeasurementStorage
    timestamp: int | None = field(init=False)

    def __post_init__(self):
        if self.storage.recent_measurement is not None:
            self.timestamp = self.storage.recent_measurement.time_range.stop


@dataclass
class GraphCandidate:
    """Graph candidate is a sub-graph that is not connected to the main graph yet.

    Contains state(s).
    """

    states: deque[State] = field(default_factory=deque)
