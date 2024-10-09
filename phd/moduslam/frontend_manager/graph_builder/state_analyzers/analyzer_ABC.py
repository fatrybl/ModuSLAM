from abc import ABC, abstractmethod

from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    State,
)
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from moduslam.utils.ordered_set import OrderedSet


class StateAnalyzer(ABC):
    """Analyzes measurements` storage and decides whether to add a new state."""

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        self._name = config.name

    @property
    def name(self) -> str:
        """Unique name of the analyzer."""
        return self._name

    @abstractmethod
    def evaluate(self, measurements: OrderedSet[Measurement]) -> State | None:
        """Evaluates the storage and decides whether to add a new state.

        Args:
            measurements: an ordered set of measurements to be analyzed.

        Returns:
            new state or None.
        """
