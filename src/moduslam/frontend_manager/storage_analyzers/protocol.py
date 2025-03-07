from typing import Protocol

from src.measurement_storage.storage import MeasurementStorage


class StorageAnalyzer(Protocol):

    @staticmethod
    def check_storage(storage: type[MeasurementStorage]) -> bool:
        """Checks if a storage has enough measurements.

        Args:
            storage: a storage to check.
        """
