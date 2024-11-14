from typing import Protocol

from phd.measurements.measurement_storage import MeasurementStorage


class StorageAnalyzer(Protocol):

    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks if a storage has enough measurements."""
