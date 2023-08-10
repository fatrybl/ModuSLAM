from csv import reader as csv_reader

from pathlib2 import Path
import cv2
from configs.paths.DEFAULT_FILE_PATHS import KaistDataset
from collections import namedtuple


class MeasurementCollector():
    def __init__(self, dataset_dir: Path):
        self.__dataset_dir = dataset_dir
        self.__create_iterators()

    def __init_iterator(self, file: Path):
        with open(file, "r") as f:
            reader = csv_reader(f)
            for position, line in enumerate(reader):
                yield position, line

    def __create_iterators(self):
        self.__iterators = {}
        file_iterator = namedtuple("file_iterator", "file iterator")
        file = self.__dataset_dir / KaistDataset.imu_data_file.value
        self.__iterators["imu"] = file_iterator(
            file, self.__init_iterator(file))
        file = self.__dataset_dir / KaistDataset.fog_data_file.value
        self.__iterators["fog"] = file_iterator(
            file, self.__init_iterator(file))
        file = self.__dataset_dir / KaistDataset.encoder_data_file.value
        self.__iterators["encoder"] = file_iterator(
            file, self.__init_iterator(file))
        file = self.__dataset_dir / KaistDataset.altimeter_data_file.value
        self.__iterators["altimeter"] = file_iterator(
            file, self.__init_iterator(file))
        file = self.__dataset_dir / KaistDataset.gps_data_file.value
        self.__iterators["gps"] = file_iterator(
            file, self.__init_iterator(file))
        file = self.__dataset_dir / KaistDataset.vrs_gps_data_file.value
        self.__iterators["vrs_gps"] = file_iterator(
            file, self.__init_iterator(file))

    def __parse_line(self, line) -> tuple:
        position, data = line
        message = {"timestamp": data[0],
                   "data": data[1:]}
        return message, position

    def __read_bin(self, file: Path) -> dict:
        with open(file, 'rb') as f:
            line = f.read()
        message = {"timestamp": file.stem,
                   "data": line}
        return message

    def get_imu(self) -> tuple:
        it = self.__iterators["imu"]
        line = next(it.iterator)
        message, position = self.__parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    def get_fog(self) -> tuple:
        it = self.__iterators["fog"]
        line = next(it.iterator)
        message, position = self.__parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    def get_encoder(self) -> tuple:
        it = self.__iterators["encoder"]
        line = next(it.iterator)
        message, position = self.__parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    def get_gps(self) -> tuple:
        it = self.__iterators["gps"]
        line = next(it.iterator)
        message, position = self.__parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    def get_vrs_gps(self) -> tuple:
        it = self.__iterators["vrs_gps"]
        line = next(it.iterator)
        message, position = self.__parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    def get_altimeter(self) -> tuple:
        it = self.__iterators["altimeter"]
        line = next(it.iterator)
        message, position = self.__parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    def get_lidar_2D(self, line: dict) -> tuple:
        sensor = line["sensor"]
        f_name = line["timestamp"]
        if sensor == 'sick_back':
            dir = KaistDataset.lidar_2D_back_dir.value
        if sensor == 'sick_middle':
            dir = KaistDataset.lidar_2D_middle_dir.value

        file = self.__dataset_dir / dir / f_name
        file = file.with_suffix('.bin')
        message = self.__read_bin(file)
        location = {"file": file}
        return message, location

    def get_lidar_3D(self, line: dict) -> dict:
        sensor = line["sensor"]
        f_name = line["timestamp"]
        if sensor == 'velodyne_right':
            dir = KaistDataset.lidar_3D_right_dir.value
        if sensor == 'velodyne_left':
            dir = KaistDataset.lidar_3D_left_dir.value

        file = self.__dataset_dir / dir / f_name
        file = file.with_suffix('.bin')
        message = self.__read_bin(file)
        location = {"file": file}
        return message, location

    def get_stereo(self, line: dict) -> tuple:
        f_name = line["timestamp"]
        left_camera_dir = self.__dataset_dir / KaistDataset.stereo_left_data_dir.value
        right_camera_dir = self.__dataset_dir / KaistDataset.stereo_right_data_dir.value

        left_img_file = self.__dataset_dir / left_camera_dir / f_name
        right_img_file = self.__dataset_dir / right_camera_dir / f_name
        left_img_file = left_img_file.with_suffix('.png')
        right_img_file = right_img_file.with_suffix('.png')

        left_img = cv2.imread(left_img_file.as_posix(), cv2.IMREAD_COLOR)
        right_img = cv2.imread(right_img_file.as_posix(), cv2.IMREAD_COLOR)

        message = {"timestamp": line["timestamp"],
                   "data": [left_img, right_img]}
        location = {"file": [left_img_file, right_img_file]}

        return message, location
