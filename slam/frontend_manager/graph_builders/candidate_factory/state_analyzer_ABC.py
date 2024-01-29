from abc import ABC, abstractmethod

from slam.frontend_manager.elements_distributor.elements_distributor import (
    MeasurementStorage,
)


class StateAnalyzer(ABC):
    """
    Analyzes processed measurements and decides whether to add a new state.
    """

    @property
    @abstractmethod
    def new_state_status(self) -> bool:
        """
        Indicates if enough measurements in storage to add a new state.
        Returns:
            (bool): new state readiness status.
        """

    @new_state_status.setter
    @abstractmethod
    def new_state_status(self, status: bool) -> None:
        """
        Sets new state status.
        Args:
            status: state status.
        """

    @abstractmethod
    def evaluate(self, storage: MeasurementStorage) -> None:
        """
        Decides whether to add a new state based on measurements in the storage.
        """
