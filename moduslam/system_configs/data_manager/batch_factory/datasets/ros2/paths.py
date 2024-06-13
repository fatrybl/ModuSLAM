from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Ros2DatasetPathConfig:
    """
    dataset format from Skoltech labs
    'https://disk.yandex.ru/d/qZxDozs23E43Hg'
    """

    sensor_data_dir = Path("sensor_data")
    image_data_dir = Path("image")
    calibration_data_dir = Path("calibration")

    data_stamp: Path = sensor_data_dir / "data_stamp.csv"
    fog_data_file: Path = sensor_data_dir / "fog.csv"
    imu_data_file: Path = sensor_data_dir / "xsens_imu.csv"
    encoder_data_file: Path = sensor_data_dir / "encoder.csv"
    altimeter_data_file: Path = sensor_data_dir / "altimeter.csv"
    lidar_2D_back_stamp_file: Path = sensor_data_dir / "SICK_back_stamp.csv"
    lidar_2D_back_dir: Path = sensor_data_dir / "SICK_back"
    lidar_2D_middle_stamp_file: Path = sensor_data_dir / "SICK_middle_stamp.csv"
    lidar_2D_middle_dir: Path = sensor_data_dir / "SICK_middle"
    lidar_3D_left_dir: Path = sensor_data_dir / "VLP_left"
    lidar_3D_right_dir: Path = sensor_data_dir / "VLP_right"
    lidar_3D_left_stamp_file: Path = sensor_data_dir / "VLP_left_stamp.csv"
    lidar_3D_right_stamp_file: Path = sensor_data_dir / "VLP_right_stamp.csv"
    stereo_stamp_file: Path = sensor_data_dir / "stereo_stamp.csv"
    vrs_gps_data_file: Path = sensor_data_dir / "vrs_gps.csv"
    gps_data_file: Path = sensor_data_dir / "gps.csv"
    stereo_left_data_dir: Path = image_data_dir / Path("stereo_left")
    stereo_right_data_dir: Path = image_data_dir / Path("stereo_right")
