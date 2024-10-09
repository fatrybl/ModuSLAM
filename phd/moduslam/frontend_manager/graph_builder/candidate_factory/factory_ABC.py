from abc import ABC, abstractmethod

from moduslam.frontend_manager.measurement_storage import MeasurementStorage


class CandidateFactory(ABC):
    """Abstract class for any candidate factory."""

    @property
    @abstractmethod
    def graph_candidate(self):
        """Graph candidate to be merged with the graph."""

    @abstractmethod
    def candidate_ready(self) -> bool:
        """Candidate readiness status."""

    @abstractmethod
    def synchronize_states(self) -> None:
        """Synchronizes states of the candidate based on metrics."""

    @abstractmethod
    def process_storage(self, storage: MeasurementStorage) -> None:
        """Processes the storage with measurements and adds new states to the graph
        candidate if needed.

        Args:
            storage: storage with measurements.
        """

    @abstractmethod
    def init_table(self, config: dict[str, str]) -> None:
        """Initializes "handler -> state analyzer" table.

        Args:
            config: config with "handler name -> state analyzer name" table.
        """
