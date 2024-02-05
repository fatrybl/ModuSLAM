from slam.frontend_manager.elements_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.criteria.criterion_ABC import (
    Criterion,
)


class LidarOdometryCriterion(Criterion):
    def check(self, storage: MeasurementStorage) -> bool:
        """
        Checks if a storage contains lidar odometry measurement.
        Args:
            storage (MeasurementStorage): a storage with processed measurements.

        Returns:
            (bool): criterion satisfaction status.
        """
        return False
