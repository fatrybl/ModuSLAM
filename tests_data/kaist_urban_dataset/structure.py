from dataclasses import dataclass, field
from pathlib import Path

from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.paths import (
    KaistDatasetPathConfig,
)


@dataclass
class DatasetStructure:

    dataset_directory: Path

    calibration_data_dir: Path = field(init=False)
    sensor_data_dir: Path = field(init=False)
    image_data_dir: Path = field(init=False)
    lidar_2D_back_dir: Path = field(init=False)
    lidar_2D_middle_dir: Path = field(init=False)
    lidar_3D_left_dir: Path = field(init=False)
    lidar_3D_right_dir: Path = field(init=False)
    stereo_left_data_dir: Path = field(init=False)
    stereo_right_data_dir: Path = field(init=False)

    data_stamp_file: Path = field(init=False)
    imu_data_file: Path = field(init=False)
    fog_data_file: Path = field(init=False)
    encoder_data_file: Path = field(init=False)
    altimeter_data_file: Path = field(init=False)
    gps_data_file: Path = field(init=False)
    vrs_gps_data_file: Path = field(init=False)
    lidar_2D_back_stamp_file: Path = field(init=False)
    lidar_2D_middle_stamp_file: Path = field(init=False)
    lidar_3D_left_stamp_file: Path = field(init=False)
    lidar_3D_right_stamp_file: Path = field(init=False)
    stereo_stamp_file: Path = field(init=False)

    binary_file_extension: str = ".bin"
    image_file_extension: str = ".png"

    def __post_init__(self):
        self.calibration_data_dir = (
            self.dataset_directory / KaistDatasetPathConfig.calibration_data_dir
        )
        self.sensor_data_dir = self.dataset_directory / KaistDatasetPathConfig.sensor_data_dir
        self.image_data_dir = self.dataset_directory / KaistDatasetPathConfig.image_data_dir
        self.data_stamp_file = self.dataset_directory / KaistDatasetPathConfig.data_stamp
        self.lidar_2D_back_dir = self.dataset_directory / KaistDatasetPathConfig.lidar_2D_back_dir
        self.lidar_2D_middle_dir = (
            self.dataset_directory / KaistDatasetPathConfig.lidar_2D_middle_dir
        )
        self.lidar_3D_left_dir = self.dataset_directory / KaistDatasetPathConfig.lidar_3D_left_dir
        self.lidar_3D_right_dir = self.dataset_directory / KaistDatasetPathConfig.lidar_3D_right_dir
        self.stereo_left_data_dir = (
            self.dataset_directory / KaistDatasetPathConfig.stereo_left_data_dir
        )
        self.stereo_right_data_dir = (
            self.dataset_directory / KaistDatasetPathConfig.stereo_right_data_dir
        )

        self.imu_data_file = self.dataset_directory / KaistDatasetPathConfig.imu_data_file
        self.fog_data_file = self.dataset_directory / KaistDatasetPathConfig.fog_data_file
        self.encoder_data_file = self.dataset_directory / KaistDatasetPathConfig.encoder_data_file
        self.altimeter_data_file = (
            self.dataset_directory / KaistDatasetPathConfig.altimeter_data_file
        )
        self.gps_data_file = self.dataset_directory / KaistDatasetPathConfig.gps_data_file
        self.vrs_gps_data_file = self.dataset_directory / KaistDatasetPathConfig.vrs_gps_data_file
        self.lidar_2D_back_stamp_file = (
            self.dataset_directory / KaistDatasetPathConfig.lidar_2D_back_stamp_file
        )
        self.lidar_2D_middle_stamp_file = (
            self.dataset_directory / KaistDatasetPathConfig.lidar_2D_middle_stamp_file
        )
        self.lidar_3D_left_stamp_file = (
            self.dataset_directory / KaistDatasetPathConfig.lidar_3D_left_stamp_file
        )
        self.lidar_3D_right_stamp_file = (
            self.dataset_directory / KaistDatasetPathConfig.lidar_3D_right_stamp_file
        )
        self.stereo_stamp_file = self.dataset_directory / KaistDatasetPathConfig.stereo_stamp_file
