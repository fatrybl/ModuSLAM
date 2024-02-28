from abc import ABC, abstractmethod

from configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State


class StateAnalyzer(ABC):
    """Analyzes processed measurements and decides whether to add a new state."""

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
