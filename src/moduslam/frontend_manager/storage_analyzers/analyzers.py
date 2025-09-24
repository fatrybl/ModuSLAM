from moduslam.frontend_manager.storage_analyzers.protocol import (
    StorageAnalyzer,
)
from moduslam.measurement_storage.measurements.pose_odometry import OdometryWithElements
from moduslam.measurement_storage.measurements.position import Position
from moduslam.measurement_storage.storage import MeasurementStorage


class SinglePoseOdometry(StorageAnalyzer):

    @staticmethod
    def check_storage(storage: type[MeasurementStorage]) -> bool:
        """Checks measurements storage if the criterion is satisfied.

        Criterion:
            1 pose odometry.

        Returns:
            check status.
        """
        data = storage.data()
        if OdometryWithElements in data:
            return True

        return False


class DoublePoseOdometry(StorageAnalyzer):

    @staticmethod
    def check_storage(storage: type[MeasurementStorage]) -> bool:
        """Checks measurements storage if the criterion is satisfied.

        Criterion:
            2 pose odometries.

        Returns:
            check status.
        """
        data = storage.data()
        if OdometryWithElements in data and len(data[OdometryWithElements]) == 2:
            return True

        return False


class QuatroPoseOdometry(StorageAnalyzer):

    @staticmethod
    def check_storage(storage: type[MeasurementStorage]) -> bool:
        """Checks measurements storage if the criterion is satisfied.

        Criterion:
            2 pose odometries.

        Returns:
            check status.
        """
        data = storage.data()
        if OdometryWithElements in data and len(data[OdometryWithElements]) == 4:
            return True

        return False


class PoseOdometryWithGps(StorageAnalyzer):

    @staticmethod
    def check_storage(storage: type[MeasurementStorage]) -> bool:
        """Checks measurements storage if the criterion is satisfied.

        Criterion:
            1 pose odometry and GPS measurements.

        Returns:
            check status.
        """
        data = storage.data()
        if (
            OdometryWithElements in data
            and Position in data
            and len(data[OdometryWithElements]) == 1
            and len(data[Position]) == 1
        ):
            return True

        return False
