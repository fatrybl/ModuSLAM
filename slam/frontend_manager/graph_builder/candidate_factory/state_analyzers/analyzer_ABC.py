from abc import ABC, abstractmethod

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.system_configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


class StateAnalyzer(ABC):
    """Analyzes measurements` storage and decides whether to add a new state."""

    @abstractmethod
    def __init__(self, config: StateAnalyzerConfig) -> None: ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the analyzer.

        Returns:
            (str): name of the analyzer.
        """

    @abstractmethod
    def evaluate(self, storage: MeasurementStorage) -> State | None:
        """
        Evaluates the storage and decides whether to add a new state.
        Args:
            storage (MeasurementStorage): storage with measurements.

        Returns:
            (State | None): new state or None.
        """
