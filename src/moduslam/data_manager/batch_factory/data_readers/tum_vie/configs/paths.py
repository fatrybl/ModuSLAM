from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TumVieDatasetPathConfig:
    """
    dataset format from
    https://cvg.cit.tum.de/data/datasets/visual-inertial-event-dataset"
    """

    calibration_file = Path("camera_calibrationA.json")
    imu_data_file = Path("imu_data.txt")
    stereo_left_images = Path("left_images")
    stereo_right_images = Path("right_images")
    stereo_left_timestamps = stereo_left_images / "image_timestamps_left.txt"
    stereo_right_timestamps = stereo_right_images / "image_timestamps_right.txt"
