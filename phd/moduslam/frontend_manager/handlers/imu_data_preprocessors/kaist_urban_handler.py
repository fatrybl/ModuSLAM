from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.config import (
    ImuHandlerConfig,
)
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.objects import (
    ImuData,
)
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.tum_vie_handler import (
    TumVieImuDataPreprocessor,
)


class KaistUrbanImuDataPreprocessor(TumVieImuDataPreprocessor):
    """Kaist Urban IMU data preprocessor."""

    def __init__(self, config: ImuHandlerConfig):
        super().__init__(config)

    @property
    def sensor_name(self) -> str:
        """Unique handler name."""
        return self._sensor_name

    @staticmethod
    def _parse_line(values: tuple[float, ...]) -> ImuData:
        """Extracts IMU data from a line of Kaist Urban dataset.

        Args:
            values: an imu data.

        Returns:
            IMU data.
        """
        angular_velocity = values[7], values[8], values[9]
        acceleration = values[10], values[11], values[12]
        return ImuData(angular_velocity, acceleration)
