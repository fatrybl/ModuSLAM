from csv import reader as csv_reader

from pathlib2 import Path
from PIL import Image

from configs.paths.DEFAULT_FILE_PATHS import KaistDataset


class MeasurementCollector():
    def __init__(self, dataset_dir: Path):
        self.__dataset_dir = dataset_dir

    def __read_line(file: Path) -> list[str]:
        with open(file, "r") as f:
            reader = csv_reader(f)
            row = next(reader)
        return row

    def get_imu(self) -> list[str]:
        file = self.__dataset_dir / KaistDataset.imu_data_file
        return self.__read_line(file)

    def get_fog(self) -> list[str]:
        file = self.__dataset_dir / KaistDataset.fog_data_file
        return self.__read_line(file)

    def get_encoder(self) -> list[str]:
        file = self.__dataset_dir / KaistDataset.encoder_data_file
        return self.__read_line(file)

    def get_lidar_2D(self) -> list[str]:
        file = self.__dataset_dir / KaistDataset.fog_data_file
        return self.__read_line(file)

    def get_lidar_3D(self) -> list[str]:
        file = self.__dataset_dir / KaistDataset.fog_data_file
        return self.__read_line(file)

    def get_gps(self) -> list[str]:
        file = self.__dataset_dir / KaistDataset.gps_data_file
        return self.__read_line(file)

    def get_vrs(self) -> list[str]:
        file = self.__dataset_dir / KaistDataset.vrs_gps_data_file
        return self.__read_line(file)

    def get_altimeter(self) -> list[str]:
        file = self.__dataset_dir / KaistDataset.altimeter_data_file
        return self.__read_line(file)

    def get_stereo(self) -> list[Image]:
        img_order_file = self.__dataset_dir / KaistDataset.stereo_stamp_file
        left_camera_dir = self.__dataset_dir / KaistDataset.stereo_left_data_dir
        right_camera_dir = self.__dataset_dir / KaistDataset.stereo_right_data_dir
        current_img_name = self.__read_line(img_order_file)
        left_img = Image.open(left_camera_dir / current_img_name / ".png")
        right_img = Image.open(right_camera_dir / current_img_name / ".png")
        return [left_img, right_img]
