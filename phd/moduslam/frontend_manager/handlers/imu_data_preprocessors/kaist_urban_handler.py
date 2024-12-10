from phd.measurement_storage.measurements.imu import ImuData
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.config import (
    ImuHandlerConfig,
)
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.tum_vie_handler import (
    TumVieImuDataPreprocessor,
)
from phd.moduslam.utils.auxiliary_methods import str_to_float


class KaistUrbanImuDataPreprocessor(TumVieImuDataPreprocessor):
    """Kaist Urban IMU data preprocessor."""

    def __init__(self, config: ImuHandlerConfig):
        super().__init__(config)

    @staticmethod
    def _parse_line(values: tuple[str, ...]) -> ImuData:
        """Extracts IMU data from a line of Kaist Urban dataset.

        Args:
            values: an imu data.

        Returns:
            IMU data.
        """
        wx = str_to_float(values[7])
        wy = str_to_float(values[8])
        wz = str_to_float(values[9])
        ax = str_to_float(values[10])
        ay = str_to_float(values[11])
        az = str_to_float(values[12])
        return ImuData((wx, wy, wz), (ax, ay, az))
