from phd.measurements.measurement_storage import MeasurementStorage
from phd.measurements.processed_measurements import Imu, PoseOdometry
from phd.moduslam.frontend_manager.measurement_storage_analyzers.base import (
    StorageAnalyzer,
)


class SinglePoseOdometry(StorageAnalyzer):

    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            1 PoseOdometry measurement exists.

        Returns:
            check status.
        """
        if PoseOdometry in storage.data:
            return True
        else:
            return False


class MultiplePoseOdometry(StorageAnalyzer):
    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            2 PoseOdometry measurements exists.

        Returns:
            check status.
        """
        if PoseOdometry in storage.data and len(storage.data[PoseOdometry]) == 2:
            return True
        else:
            return False


class SingleLidarOdometryWithImu(StorageAnalyzer):
    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            1 lidar PoseOdometry and IMU measurements.

        Returns:
            check status.
        """
        if (
            PoseOdometry in storage.data
            and Imu in storage.data
            and len(storage.data[PoseOdometry]) == 1
            and len(storage.data[Imu]) > 0
        ):
            return True
        else:
            return False
