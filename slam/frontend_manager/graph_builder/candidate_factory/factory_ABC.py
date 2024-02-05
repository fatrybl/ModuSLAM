from abc import ABC, abstractmethod

from slam.frontend_manager.elements_distributor.measurement_storage import (
    MeasurementStorage,
)


class CandidateFactory(ABC):
    """
    Abstract class for any candidate factory.
    """

    @property
    @abstractmethod
    def graph_candidate(self):
        """
        Graph candidate.
        Returns:
            (GraphCandidate): graph candidate.
        """
        ...

    @abstractmethod
    def candidate_ready(self) -> bool:
        """
        Candidate readiness status.
        Returns:
            (bool): graph candidate readiness status.
        """
        ...

    @abstractmethod
    def synchronize_states(self) -> None:
        """
        Synchronizes states of the candidate based on criteria.
        """
        ...

    @abstractmethod
    def process_storage(self, storage: MeasurementStorage) -> None:
        """
        Processes input measurements and adds new states to the graph candidate if a criterion is satisfied.

        1) Check if a criterion for a new state is met for every criteria.
        2) If a criterion, add a new state to the graph candidate.

        Args:
            storage (MeasurementStorage): processed measurements from the Distributor.
        """
        ...
