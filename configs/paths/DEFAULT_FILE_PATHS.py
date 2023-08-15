from enum import Enum
from pathlib2 import Path


class ConfigFilePaths(Enum):
    root_path = Path(__file__).parent.parent
    data_manager_config = root_path / "system/data_manager/data_manager.yaml"
    data_reader_config = root_path / "system/data_manager/data_readers.yaml"


class KaistDataset(Enum):
    """
    dataset format from 
    https://sites.google.com/view/complex-urban-dataset/format"
    """
    sensor_data_dir = Path("sensor_data")
    image_data_dir = Path("image")
    calibration_data_dir = Path("calibration")

    data_stamp = sensor_data_dir / "test_data_stamp.csv"
    fog_data_file = sensor_data_dir / "fog.csv"
    imu_data_file = sensor_data_dir / "xsens_imu.csv"
    encoder_data_file = sensor_data_dir / "encoder.csv"
    altimeter_data_file = sensor_data_dir / "altimeter.csv"
    lidar_2D_back_stamp_file = sensor_data_dir / "SICK_back_stamp.csv"
    lidar_2D_back_dir = sensor_data_dir / "SICK_back"
    lidar_2D_middle_stamp_file = sensor_data_dir / "SICK_middle_stamp.csv"
    lidar_2D_middle_dir = sensor_data_dir / "SICK_middle"
    lidar_3D_left_dir = sensor_data_dir / "VLP_left"
    lidar_3D_right_dir = sensor_data_dir / "VLP_right"
    lidar_3D_left_stamp_file = sensor_data_dir / "VLP_left_stamp.csv"
    lidar_3D_right_stamp_file = sensor_data_dir / "VLP_right_stamp.csv"
    stereo_stamp_file = sensor_data_dir / "stereo_stamp.csv"
    vrs_gps_data_file = sensor_data_dir / "vrs_gps.csv"
    gps_data_file = sensor_data_dir / "gps.csv"
    stereo_left_data_dir = image_data_dir / "stereo_left"
    stereo_right_data_dir = image_data_dir / "stereo_right"

class RosDataset(Enum):
    """
    dataset format from 
    https://projects.asl.ethz.ch/datasets/doku.php?id=laserregistration:laserregistration
    """

    imu_data_topic =  '/imu_data' # ['/imu1']
    gps_data_topic = '/position_gps'
    gps_info_topic = '/info_gps'

    data_stamp = Path('0-Tiltlaser.bag')