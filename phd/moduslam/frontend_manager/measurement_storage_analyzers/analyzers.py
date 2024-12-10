from phd.measurement_storage.measurements.gps import Gps
from phd.measurement_storage.measurements.imu import ProcessedImu
from phd.measurement_storage.measurements.pose_odometry import OdometryWithElements
from phd.measurement_storage.storage import MeasurementStorage
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
        if OdometryWithElements in storage.data:
            return True

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
        if OdometryWithElements in storage.data and len(storage.data[OdometryWithElements]) == 2:
            return True

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
            OdometryWithElements in storage.data
            and ProcessedImu in storage.data
            and len(storage.data[OdometryWithElements]) == 1
            and len(storage.data[ProcessedImu]) > 0
        ):
            return True

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
            OdometryWithElements in storage.data
            and ProcessedImu in storage.data
            and len(storage.data[OdometryWithElements]) == 2
            and len(storage.data[ProcessedImu]) > 0
        ):
            return True

        return False


class PoseOdometryWithGps(StorageAnalyzer):
    @staticmethod
    def check_storage(storage: MeasurementStorage) -> bool:
        """Checks measurements storage if the criterion is satisfied.
        Criterion:
            1 pose odometry and GPS measurements.

        Returns:
            check status.
        """
        if (
            OdometryWithElements in storage.data
            and Gps in storage.data
            and len(storage.data[OdometryWithElements]) == 1
            and len(storage.data[Gps]) == 1
        ):
            return True

        return False
