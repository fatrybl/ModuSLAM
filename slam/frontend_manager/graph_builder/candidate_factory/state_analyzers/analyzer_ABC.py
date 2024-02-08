from abc import ABC, abstractmethod

from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.criteria.criterion_ABC import (
    Criterion,
)


class StateAnalyzer(ABC):
    """
    Analyzes processed measurements and decides whether to add a new state.
    """

    @property
    @abstractmethod
    def criteria(self) -> list[Criterion]:
        """
        All criteria.
        Returns:
            (list): list of criteria.
        """

    #
    # @property
    # @abstractmethod
    # def new_state_status(self) -> bool:
    #     """
    #     Indicates if enough measurements in storage to add a new state.
    #     Returns:
    #         (bool): new state readiness status.
    #     """
    #
    # @new_state_status.setter
    # @abstractmethod
    # def new_state_status(self, status: bool) -> None:
    #     """
    #     Sets new state status.
    #     Args:
    #         status: state status.
    #     """
    #
    # @abstractmethod
    # def evaluate(self, storage: MeasurementStorage) -> State | None:
    #     """
    #     Decides whether to create a new state based on measurements in the storage.
    #     """
