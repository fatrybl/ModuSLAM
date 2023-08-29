import logging
from collections import namedtuple

from csv import reader as csv_reader
from pathlib import Path
from cv2 import imread, IMREAD_COLOR
from plum import dispatch

from configs.paths.DEFAULT_FILE_PATHS import KaistDataset

logger = logging.getLogger(__name__)


class MeasurementCollector():
    def __init__(self, dataset_dir: Path):
        self._dataset_dir = dataset_dir
        self._create_iterators()

    def _init_iterator(self, file: Path):
        with open(file, "r") as f:
            reader = csv_reader(f)
            for position, line in enumerate(reader):
                yield position, line

    def _reset_iterators(self) -> None:
        self._create_iterators()

    def _create_iterators(self) -> None:
        self._iterators = {}
        file_iterator = namedtuple("file_iterator", "file iterator")
        file = self._dataset_dir / KaistDataset.imu_data_file.value
        self._iterators["imu"] = file_iterator(
            file, self._init_iterator(file))
        file = self._dataset_dir / KaistDataset.fog_data_file.value
        self._iterators["fog"] = file_iterator(
            file, self._init_iterator(file))
        file = self._dataset_dir / KaistDataset.encoder_data_file.value
        self._iterators["encoder"] = file_iterator(
            file, self._init_iterator(file))
        file = self._dataset_dir / KaistDataset.altimeter_data_file.value
        self._iterators["altimeter"] = file_iterator(
            file, self._init_iterator(file))
        file = self._dataset_dir / KaistDataset.gps_data_file.value
        self._iterators["gps"] = file_iterator(
            file, self._init_iterator(file))
        file = self._dataset_dir / KaistDataset.vrs_gps_data_file.value
        self._iterators["vrs_gps"] = file_iterator(
            file, self._init_iterator(file))

    def _parse_line(self, line) -> tuple:
        position, data = line
        message = {"timestamp": data[0],
                   "data": data[1:]}
        return message, position

    def _read_bin(self, file: Path) -> dict:
        with open(file, 'rb') as f:
            line = f.read()
            message = {"timestamp": file.stem,
                       "data": line}
            return message

    def _find_in_file(self, it, timestamp: int) -> dict[str, str]:
        while current_timestamp != timestamp:
            line = next(it.iterator)
            _, data = line
            current_timestamp = data[0]
        return line

    @dispatch
    def get_imu(self) -> tuple[dict, dict]:
        it = self._iterators["imu"]
        line = next(it.iterator)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_imu(self, timestamp: int) -> tuple[dict, dict]:
        it = self._iterators["imu"]
        line = self._find_in_file(it, timestamp)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_fog(self) -> tuple[dict, dict]:
        it = self._iterators["fog"]
        line = next(it.iterator)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_fog(self, timestamp: int) -> tuple[dict, dict]:
        it = self._iterators["fog"]
        line = self._find_in_file(it, timestamp)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_encoder(self) -> tuple[dict, dict]:
        it = self._iterators["encoder"]
        line = next(it.iterator)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_encoder(self, timestamp: int) -> tuple[dict, dict]:
        it = self._iterators["encoder"]
        line = self._find_in_file(it, timestamp)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_gps(self) -> tuple[dict, dict]:
        it = self._iterators["gps"]
        line = next(it.iterator)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_gps(self, timestamp: int) -> tuple[dict, dict]:
        it = self._iterators["gps"]
        line = self._find_in_file(it, timestamp)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_vrs_gps(self) -> tuple[dict, dict]:
        it = self._iterators["vrs_gps"]
        line = next(it.iterator)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_vrs_gps(self, timestamp: int) -> tuple[dict, dict]:
        it = self._iterators["vrs_gps"]
        line = self._find_in_file(it, timestamp)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_altimeter(self) -> tuple[dict, dict]:
        it = self._iterators["altimeter"]
        line = next(it.iterator)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    @dispatch
    def get_altimeter(self, timestamp: int) -> tuple[dict, dict]:
        it = self._iterators["altimeter"]
        line = self._find_in_file(it, timestamp)
        message, position = self._parse_line(line)
        location = {"file": it.file,
                    "position": position}
        return message, location

    def _get_lidar(self, timestamp, dir):
        f_name = timestamp
        file = self._dataset_dir / dir / f_name
        file = file.with_suffix('.bin')
        message = self._read_bin(file)
        location = {"file": file}
        return message, location

    def get_lidar_2D_sick_back(self, timestamp: str) -> tuple[dict, dict]:
        dir = KaistDataset.lidar_2D_back_dir.value
        return self._get_lidar(timestamp, dir)

    def get_lidar_2D_sick_middle(self, timestamp: str) -> tuple[dict, dict]:
        dir = KaistDataset.lidar_2D_middle_dir.value
        return self._get_lidar(timestamp, dir)

    def get_lidar_3D_velodyne_left(self, timestamp: str) -> tuple[dict, dict]:
        dir = KaistDataset.lidar_3D_left_dir.value
        return self._get_lidar(timestamp, dir)

    def get_lidar_3D_velodyne_right(self, timestamp: str) -> tuple[dict, dict]:
        dir = KaistDataset.lidar_3D_right_dir.value
        return self._get_lidar(timestamp, dir)

    def get_stereo(self, timestamp: str) -> tuple[dict, dict]:
        f_name = timestamp
        left_camera_dir = self._dataset_dir / KaistDataset.stereo_left_data_dir.value
        right_camera_dir = self._dataset_dir / KaistDataset.stereo_right_data_dir.value

        left_img_file = self._dataset_dir / left_camera_dir / f_name
        right_img_file = self._dataset_dir / right_camera_dir / f_name
        left_img_file = left_img_file.with_suffix('.png')
        right_img_file = right_img_file.with_suffix('.png')

        left_img = imread(left_img_file.as_posix(), IMREAD_COLOR)
        right_img = imread(right_img_file.as_posix(), IMREAD_COLOR)

        message = {"timestamp": timestamp,
                   "data": [left_img, right_img]}
        location = {"file": [left_img_file, right_img_file]}

        return message, location

    def _get_reader(self, sensor: str):
        if sensor == "imu":
            return self.get_imu
        elif sensor == "fog":
            return self.get_fog
        elif sensor == "encoder":
            return self.get_encoder
        elif sensor == "gps":
            return self.get_gps
        elif sensor == "vrs":
            return self.get_vrs_gps
        elif sensor == "altimeter":
            return self.get_altimeter
        elif sensor == "sick_back":
            return self.get_lidar_2D_sick_back
        elif sensor == "sick_middle":
            return self.get_lidar_2D_sick_middle
        elif sensor == "velodyne_right":
            return self.get_lidar_3D_velodyne_right
        elif sensor == "velodyne_left":
            return self.get_lidar_3D_velodyne_left
        elif sensor == "stereo":
            return self.get_stereo
        else:
            logger.critical(f"no method to parse data for sensor: {sensor}")
            raise KeyError

    @dispatch
    def get_data(self, line: dict[str, str]) -> tuple[dict, dict]:
        """
        Gets raw data sequantically by iterating over lines in files
        Args:
            line: dict[str, str]: line in file with sensor`s name and timestamp
        Returns: 
            tuple[dict, dict]: message with raw data and location
        """
        timestamp = line['timestamp']
        sensor = line['sensor']
        data_reader = self._get_reader(sensor)
        if sensor in self._iterators.keys():
            message, location = data_reader()
        else:
            message, location = data_reader(timestamp)

        return message, location

    @dispatch
    def get_data_by_measurement(self, line: dict[str, str | int]) -> tuple[dict, dict]:
        """
        Gets raw data based on input measurement
        Args:
            line: dict[str, str]: line in file with sensor`s name and timestamp
        Returns: 
            tuple[dict, dict]: message with raw data and location
        """
        print('sadsfsdfsdsdsdsd')
        timestamp = line['timestamp']
        sensor = line['sensor']
        if isinstance(timestamp, int):
            timestamp = str(timestamp)

        data_reader = self._get_reader(sensor)
        message, location = data_reader(timestamp)

        self._reset_iterators()
        return message, location
