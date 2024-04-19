from abc import ABC, abstractmethod

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)


class CandidateFactory(ABC):
    """Abstract class for any candidate factory."""

    @property
    @abstractmethod
    def graph_candidate(self):
        """Graph candidate.

        Returns:
            (GraphCandidate): graph candidate.
        """

    @abstractmethod
    def candidate_ready(self) -> bool:
        """Candidate readiness status.

        Returns:
            graph candidate readiness status (bool).
        """

    @abstractmethod
    def synchronize_states(self) -> None:
        """Synchronizes states of the candidate based on criteria."""

    @abstractmethod
    def process_storage(self, storage: MeasurementStorage) -> None:
        """Processes input measurements and adds new states to the graph candidate if a
        criterion is satisfied.

        Args:
            storage (MeasurementStorage): processed measurements from the Distributor.
        """

    @abstractmethod
    def init_table(self, config: dict[str, str]) -> None:
        """Initializes the table: handler -> state analyzer.

        Args:
            config (dict[str, str]): table with names of handlers and state analyzers.
        """
