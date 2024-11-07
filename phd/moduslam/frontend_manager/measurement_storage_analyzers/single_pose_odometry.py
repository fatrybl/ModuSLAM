from phd.measurements.measurement_storage import MeasurementStorage
from phd.measurements.processed_measurements import PoseOdometry


class Analyzer:

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
