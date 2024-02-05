from abc import ABC, abstractmethod

from slam.frontend_manager.elements_distributor.measurement_storage import (
    MeasurementStorage,
)


class Criterion(ABC):
    """
    Abstract class for a criterion of a new state.
    """

    @abstractmethod
    def check(self, storage: MeasurementStorage) -> bool:
        """
        Checks if a criterion is satisfied.
        Args:
            storage (MeasurementStorage): a storage with processed measurements.

        Returns:
            (bool): criterion satisfaction status.
        """
