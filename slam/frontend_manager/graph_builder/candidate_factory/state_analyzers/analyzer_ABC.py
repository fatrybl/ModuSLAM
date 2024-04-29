from abc import ABC, abstractmethod

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


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
    def evaluate(self, storage: MeasurementStorage) -> State | None:
        """Evaluates the storage and decides whether to add a new state.

        Args:
            storage: a storage with measurements.

        Returns:
            new state or None.
        """
