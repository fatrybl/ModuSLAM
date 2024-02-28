from dataclasses import dataclass, field
from pathlib import Path

from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.paths import (
    KaistDatasetPathConfig as KaistPaths,
)


@dataclass
class KaistConfig(DatasetConfig):
    """Kaist Urban Dataset parameters."""

    directory: Path = field(kw_only=True)

    csv_files_table: dict[str, Path] = field(
        metadata={"description": "table of: {<SENSOR_NAME>, <CSV_FILE_PATH>}"},
        default_factory=lambda: {
            "imu": KaistPaths.imu_data_file,
            "encoder": KaistPaths.encoder_data_file,
            "gps": KaistPaths.gps_data_file,
            "vrs": KaistPaths.vrs_gps_data_file,
            "fog": KaistPaths.fog_data_file,
            "altimeter": KaistPaths.altimeter_data_file,
            "sick_back": KaistPaths.lidar_2D_back_stamp_file,
            "sick_middle": KaistPaths.lidar_2D_middle_stamp_file,
            "velodyne_left": KaistPaths.lidar_3D_left_stamp_file,
            "velodyne_right": KaistPaths.lidar_3D_right_stamp_file,
            "stereo": KaistPaths.stereo_stamp_file,
        },
    )

    lidar_data_dir_table: dict[str, Path] = field(
        metadata={"description": "table of: {<SENSOR_NAME>, <LIDAR_DATA_DIRECTORY_PATH>}"},
        default_factory=lambda: {
            "sick_back": KaistPaths.lidar_2D_back_dir,
            "sick_middle": KaistPaths.lidar_2D_middle_dir,
            "velodyne_left": KaistPaths.lidar_3D_left_dir,
            "velodyne_right": KaistPaths.lidar_3D_right_dir,
        },
    )

    stereo_data_dir_table: dict[str, Path] = field(
        metadata={"description": "table of: {<SENSOR_NAME>, <STEREO_DATA_DIRECTORY_PATH>}"},
        default_factory=lambda: {
            "stereo_left_camera": KaistPaths.stereo_left_data_dir,
            "stereo_right_camera": KaistPaths.stereo_right_data_dir,
        },
    )

    data_stamp_file: Path = KaistPaths.data_stamp

    reader: str = "KaistReader"

    name: str = "Kaist Urban Dataset"

    url: str = "https://sites.google.com/view/complex-urban-dataset"
