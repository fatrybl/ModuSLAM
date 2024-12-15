from dataclasses import dataclass, field
from pathlib import Path

from phd.moduslam.data_manager.batch_factory.configs import DataReaders, DatasetConfig
from phd.moduslam.data_manager.batch_factory.readers.kaist.configs.paths import (
    KaistDatasetPathConfig as KaistPaths,
)


@dataclass
class KaistConfig(DatasetConfig):
    """Base Kaist Urban Dataset configuration."""

    directory: Path = Path()

    reader: str = DataReaders.kaist_reader

    name: str = "Kaist Urban Dataset"

    url: str = "https://sites.google.com/view/complex-urban-dataset"

    imu_name: str = "imu"
    encoder_name: str = "encoder"
    gps_name: str = "gps"
    vrs_gps_name: str = "vrs"
    fog_name: str = "fog"
    altimeter_name: str = "altimeter"
    lidar_2D_back_name: str = "sick_back"
    lidar_2D_middle_name: str = "sick_middle"
    lidar_3D_left_name: str = "velodyne_left"
    lidar_3D_right_name: str = "velodyne_right"
    stereo_name: str = "stereo"

    data_stamp_file: Path = KaistPaths.data_stamp

    csv_files: dict[str, Path] = field(
        default_factory=lambda: {
            KaistConfig.imu_name: KaistPaths.imu_data_file,
            KaistConfig.encoder_name: KaistPaths.encoder_data_file,
            KaistConfig.gps_name: KaistPaths.gps_data_file,
            KaistConfig.vrs_gps_name: KaistPaths.vrs_gps_data_file,
            KaistConfig.fog_name: KaistPaths.fog_data_file,
            KaistConfig.altimeter_name: KaistPaths.altimeter_data_file,
            KaistConfig.lidar_2D_back_name: KaistPaths.lidar_2D_back_stamp_file,
            KaistConfig.lidar_2D_middle_name: KaistPaths.lidar_2D_middle_stamp_file,
            KaistConfig.lidar_3D_left_name: KaistPaths.lidar_3D_left_stamp_file,
            KaistConfig.lidar_3D_right_name: KaistPaths.lidar_3D_right_stamp_file,
            KaistConfig.stereo_name: KaistPaths.stereo_stamp_file,
        },
    )

    lidar_data_dirs: dict[str, Path] = field(
        default_factory=lambda: {
            KaistConfig.lidar_2D_back_name: KaistPaths.lidar_2D_back_dir,
            KaistConfig.lidar_2D_middle_name: KaistPaths.lidar_2D_middle_dir,
            KaistConfig.lidar_3D_left_name: KaistPaths.lidar_3D_left_dir,
            KaistConfig.lidar_3D_right_name: KaistPaths.lidar_3D_right_dir,
        },
    )

    stereo_data_dirs: list[Path] = field(
        default_factory=lambda: [KaistPaths.stereo_left_data_dir, KaistPaths.stereo_right_data_dir],
    )
