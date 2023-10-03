import csv

from array import array

from yaml import safe_dump
from pathlib import Path
from numpy import array as numpy_array
from cv2 import imwrite
from shutil import copyfile, copytree

from configs.paths.default import ConfigPaths


class TestDataFactory:
    CURRENT_DIR = Path(__file__).parent
    TEST_DATA_DIR: Path = CURRENT_DIR / 'test_data'
    DEFAULT_SENSORS_CONFIG_DIR: Path = ConfigPaths.sensors_config_dir.value
    MODIFIED_SENSORS_CONFIG_DIR: Path = DEFAULT_SENSORS_CONFIG_DIR.parent / \
        (DEFAULT_SENSORS_CONFIG_DIR.stem + '_original')
    DEFAULT_DATAMANAGER_CONFIG_PATH: Path = ConfigPaths.data_manager_config.value
    MODIFIED_DATAMANAGER_CONFIG_NAME: Path = DEFAULT_DATAMANAGER_CONFIG_PATH.stem + '_original.yaml'
    MODIFIED_DATAMANAGER_CONFIG_PATH: Path = DEFAULT_DATAMANAGER_CONFIG_PATH.parent / \
        MODIFIED_DATAMANAGER_CONFIG_NAME

    sensors = {
        "fog": {
            "type": "fog",
            "config": "fog.yaml"},

        "imu": {
            "type": "imu",
            "config": "imu.yaml"},

        "encoder": {
            "type": "encoder",
                    "config": "encoder.yaml"},

        "altimeter": {
            "type": "altimeter",
                    "config": "altimeter.yaml"},

        "gps": {
            "type": "gps",
                    "config": "gps.yaml"},

        "vrs": {
            "type": "vrs_gps",
                    "config": "vrs.yaml"},

        "sick_back": {
            "type": "lidar_2D",
                    "config": "sick_back.yaml"},

        "sick_middle": {
            "type": "lidar_2D",
                    "config": "sick_middle.yaml"},

        "velodyne_left": {
            "type": "lidar_3D",
                    "config": "velodyne_left.yaml"},

        "velodyne_right": {
            "type": "lidar_3D",
                    "config": "velodyne_right.yaml"},

        "stereo": {
            "type": "stereo_camera",
                    "config": "stereo.yaml"}, }

    data_stamp = [
        ['1234', 'imu'],
        ['1234', 'fog'],
        ['1234', 'gps'],
        ['1234', 'vrs'],
        ['1234', 'altimeter'],
        ['1234', 'encoder'],
        ['1234', 'sick_back'],
        ['1234', 'sick_middle'],
        ['1234', 'velodyne_left'],
        ['1234', 'velodyne_right'],
        ['1234', 'stereo']
    ]

    imu = [1234, 0.1234, -0.1234, 0.1234]
    fog = [1234, 0.1234, -0.1234, 0.1234]
    gps = [1234, 0.1234, -0.1234, 0.1234]
    vrs_gps = [1234, 0.1234, -0.1234, 0.1234]
    altimeter = [1234, 0.1234, -0.1234, 0.1234]
    encoder = [1234, 0.1234, -0.1234, 0.1234]
    sick_back = [1234, 0.1234, -0.1234, 0.1234]
    sick_middle = [1234, 0.1234, -0.1234, 0.1234]
    velodyne_left = [1234, 0.1234, -0.1234, 0.1234]
    velodyne_right = [1234, 0.1234, -0.1234, 0.1234]
    stereo_left = [0, 255, 255, 0]
    stereo_right = [0, 255, 255, 0]

    sensor_data_dir = TEST_DATA_DIR / 'sensor_data'

    binary_data = [(sick_back, sensor_data_dir / 'SICK_back'),
                   (sick_middle, sensor_data_dir / 'SICK_middle'),
                   (velodyne_left, sensor_data_dir / 'VLP_left'),
                   (velodyne_right, sensor_data_dir / 'VLP_right')
                   ]
    png_data = [(stereo_left, TEST_DATA_DIR / 'image' / 'stereo_left'),
                (stereo_right, TEST_DATA_DIR / 'image' / 'stereo_right'),]

    csv_data = [(imu, sensor_data_dir / 'xsens_imu.csv'),
                (fog, sensor_data_dir / 'fog.csv'),
                (gps, sensor_data_dir / 'gps.csv'),
                (vrs_gps, sensor_data_dir / 'vrs_gps.csv'),
                (altimeter, sensor_data_dir / 'altimeter.csv'),
                (encoder, sensor_data_dir / 'encoder.csv'),]

    @classmethod
    def to_bytes_array(cls, floats: list[float]) -> bytes:
        return array('d', floats).tobytes()

    @classmethod
    def to_binary_file(cls, data: list[float], path: Path) -> None:
        with open(path, 'wb') as output_file:
            float_array = array('d', data)
            float_array.tofile(output_file)

    @classmethod
    def to_csv_file(cls, data: list[float | list[str]], path: Path, multilines: bool = False) -> None:
        with open(path, 'w', encoding='UTF8', newline='') as outfile:
            writer = csv.writer(outfile)
            if multilines:
                writer.writerows(data)
            else:
                writer.writerow(data)

    @classmethod
    def to_png_file(cls, data: list[int], path: Path) -> None:
        data = numpy_array(data).reshape(2, 2)
        imwrite(path.as_posix(), data)

    @classmethod
    def create_sensors_config_files(cls) -> None:
        """
        Copies ".../sensors/" directory with configs to ".../sensors_original/".
        Creates test config files for sensors
        """
        test_params = {"pose": (1, 2, 3, 4)}
        src: Path = cls.DEFAULT_SENSORS_CONFIG_DIR
        dst: Path = cls.MODIFIED_SENSORS_CONFIG_DIR
        copytree(src, dst, dirs_exist_ok=True)

        for config_data in cls.sensors.values():
            path = src / config_data['config']
            with open(path, 'w') as f:
                safe_dump(test_params, f)

    def prepare_data(self,) -> None:
        self.TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

        Path.mkdir(self.TEST_DATA_DIR / 'calibration',
                   parents=True, exist_ok=True)
        Path.mkdir(self.TEST_DATA_DIR / 'image', parents=True, exist_ok=True)
        Path.mkdir(self.TEST_DATA_DIR / 'sensor_data',
                   parents=True, exist_ok=True)

        Path.mkdir(self.TEST_DATA_DIR / 'image' /
                   'stereo_left', parents=True, exist_ok=True)
        Path.mkdir(self.TEST_DATA_DIR / 'image' /
                   'stereo_right', parents=True, exist_ok=True)

        Path.mkdir(self.sensor_data_dir / 'SICK_back',
                   parents=True, exist_ok=True)
        Path.mkdir(self.sensor_data_dir / 'SICK_middle',
                   parents=True, exist_ok=True)
        Path.mkdir(self.sensor_data_dir / 'VLP_left',
                   parents=True, exist_ok=True)
        Path.mkdir(self.sensor_data_dir / 'VLP_right',
                   parents=True, exist_ok=True)

        test_data_stamp_file = self.sensor_data_dir / "data_stamp.csv"
        self.to_csv_file(
            self.data_stamp, test_data_stamp_file, multilines=True)

        for element, path in self.csv_data:
            self.to_csv_file(element, path)

        for element, path in self.binary_data:
            self.to_binary_file(element, path / '1234.bin')

        for element, path in self.png_data:
            self.to_png_file(element, path / '1234.png')

        self.create_sensors_config_files()

    def modify_default_config(self,) -> None:
        """
        1) copy 'data_manager.yaml "data_manager_original.yaml"
        2) write test config to 'data_manager.yaml'
        """
        copyfile(self.DEFAULT_DATAMANAGER_CONFIG_PATH,
                 self.MODIFIED_DATAMANAGER_CONFIG_PATH)

        test_dataset_dir = self.CURRENT_DIR / "test_data"
        test_params = {"data":
                       {
                           "dataset_type": "kaist",
                           "dataset_directory":  test_dataset_dir.as_posix()
                       },
                       "sensors": self.sensors}

        with open(self.DEFAULT_DATAMANAGER_CONFIG_PATH, 'w') as outfile:
            safe_dump(test_params, outfile)
