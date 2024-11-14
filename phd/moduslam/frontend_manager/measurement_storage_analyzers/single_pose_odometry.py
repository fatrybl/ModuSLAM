from phd.measurements.measurement_storage import MeasurementStorage
from phd.measurements.processed_measurements import PoseOdometry
from phd.moduslam.frontend_manager.measurement_storage_analyzers.base import (
    StorageAnalyzer,
)


class Analyzer(StorageAnalyzer):

    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            1 PoseOdometry measurement exists.

        Returns:
            check status.
        """
        if storage.data[PoseOdometry]:
            return True
        else:
            return False
