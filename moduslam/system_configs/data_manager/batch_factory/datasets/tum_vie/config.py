from dataclasses import dataclass, field
from pathlib import Path

from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.paths import (
    TumVieDatasetPathConfig as TumPaths,
)


@dataclass
class TumVieConfig(DatasetConfig):
    """Kaist Urban Dataset parameters."""

    directory: Path = Path("")

    reader: str = "TumVieReader"

    name: str = "TUM Visual-Inertial Event Dataset"

    url: str = "https://cvg.cit.tum.de/data/datasets/visual-inertial-event-dataset"

    imu_name: str = "imu"
    stereo_name: str = "stereo"

    csv_files: dict[str, Path] = field(
        metadata={"description": "table of: {<SENSOR_NAME>, <CSV_FILE_PATH>}"},
        default_factory=lambda: {
            TumVieConfig.imu_name: TumPaths.imu_data_file,
            TumVieConfig.stereo_name: TumPaths.stereo_left_timestamps,
        },
    )

    stereo_data_dirs: list[Path] = field(
        default_factory=lambda: [TumPaths.stereo_left_images, TumPaths.stereo_right_images],
    )
