from collections import deque
from dataclasses import dataclass, field

from slam.frontend_manager.elements_distributor.elements_distributor import (
    MeasurementStorage,
)


@dataclass
class State:
    storage: MeasurementStorage
    timestamp: int = field(init=False)

    def __post_init__(self):
        self.timestamp = self.storage.last_timestamp


@dataclass
class GraphCandidate:
    states: deque[State] = deque()
