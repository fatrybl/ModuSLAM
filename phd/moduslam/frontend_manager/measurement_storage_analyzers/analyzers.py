from phd.measurements.processed import Imu, PoseOdometry
from phd.measurements.storage import MeasurementStorage
from phd.moduslam.frontend_manager.measurement_storage_analyzers.base import (
    StorageAnalyzer,
)


class SinglePoseOdometry(StorageAnalyzer):

    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            1 pose odometry.

        Returns:
            check status.
        """
        if PoseOdometry in storage.data:
            return True
        else:
            return False


class DoublePoseOdometry(StorageAnalyzer):
    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            2 pose odometries.

        Returns:
            check status.
        """
        if PoseOdometry in storage.data and len(storage.data[PoseOdometry]) == 2:
            return True
        else:
            return False


class SinglePoseOdometryWithImu(StorageAnalyzer):
    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            1 pose odometry and IMU measurements.

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


class DoublePoseOdometryWithImu(StorageAnalyzer):
    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            2 pose odometries and IMU measurements.

        Returns:
            check status.
        """
        if (
            PoseOdometry in storage.data
            and Imu in storage.data
            and len(storage.data[PoseOdometry]) == 2
            and len(storage.data[Imu]) > 0
        ):
            return True
        else:
            return False
