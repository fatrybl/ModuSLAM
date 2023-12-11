from collections import deque
from dataclasses import dataclass

from slam.frontend_manager.elements_distributor.elements_distributor import MeasurementStorage


@dataclass
class State:
    timestamp: int
    storage: MeasurementStorage


@dataclass
class GraphCandidate:
    states: deque[State] = deque()
