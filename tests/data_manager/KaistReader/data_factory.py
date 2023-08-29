import csv

from array import array
from yaml import safe_dump
from pathlib import Path
from numpy import array as numpy_array
from cv2 import imwrite

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths


class TestDataFactory:
    CURRENT_DIR = Path(__file__).parent
    TEST_DATA_DIR = CURRENT_DIR / 'test_data'
    DEFAULT_DATAMANAGER_CONFIG_PATH = ConfigFilePaths.data_manager_config.value
    MODIFIED_DATAMANAGER_CONFIG_NAME = DEFAULT_DATAMANAGER_CONFIG_PATH.stem + '_original.yaml'
    MODIFIED_DATAMANAGER_CONFIG_PATH = DEFAULT_DATAMANAGER_CONFIG_PATH.parent / \
        MODIFIED_DATAMANAGER_CONFIG_NAME

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

    def prepare_data(self,) -> None:
        test_dataset_dir = TestDataFactory.CURRENT_DIR / "test_data"
        test_dataset_dir.mkdir(parents=True, exist_ok=True)

        Path.mkdir(test_dataset_dir / 'calibration',
                   parents=True, exist_ok=True)
        Path.mkdir(test_dataset_dir / 'image', parents=True, exist_ok=True)
        Path.mkdir(test_dataset_dir / 'sensor_data',
                   parents=True, exist_ok=True)

        Path.mkdir(test_dataset_dir / 'image' /
                   'stereo_left', parents=True, exist_ok=True)
        Path.mkdir(test_dataset_dir / 'image' /
                   'stereo_right', parents=True, exist_ok=True)

        sensor_data_dir = test_dataset_dir / 'sensor_data'

        Path.mkdir(sensor_data_dir / 'SICK_back', parents=True, exist_ok=True)
        Path.mkdir(sensor_data_dir / 'SICK_middle',
                   parents=True, exist_ok=True)
        Path.mkdir(sensor_data_dir / 'VLP_left', parents=True, exist_ok=True)
        Path.mkdir(sensor_data_dir / 'VLP_right', parents=True, exist_ok=True)

        test_data_stamp = [
            ['1234', 'imu'],
            ['1234', 'fog'],
            ['1234', 'gps'],
            ['1234', 'vrs_gps'],
            ['1234', 'altimeter'],
            ['1234', 'encoder'],
            ['1234', 'sick_back'],
            ['1234', 'sick_middle'],
            ['1234', 'velodyne_left'],
            ['1234', 'velodyne_right'],
            ['1234', 'stereo']
        ]
        test_data_stamp_file = sensor_data_dir / "data_stamp.csv"
        self.to_csv_file(
            test_data_stamp, test_data_stamp_file, multilines=True)

        test_imu = [1234, 0.1234, -0.1234, 0.1234]
        test_fog = [1234, 0.1234, -0.1234, 0.1234]
        test_gps = [1234, 0.1234, -0.1234, 0.1234]
        test_vrs_gps = [1234, 0.1234, -0.1234, 0.1234]
        test_altimeter = [1234, 0.1234, -0.1234, 0.1234]
        test_encoder = [1234, 0.1234, -0.1234, 0.1234]
        test_sick_back = [1234, 0.1234, -0.1234, 0.1234]
        test_sick_middle = [1234, 0.1234, -0.1234, 0.1234]
        test_velodyne_left = [1234, 0.1234, -0.1234, 0.1234]
        test_velodyne_right = [1234, 0.1234, -0.1234, 0.1234]
        test_stereo_left = [0, 255, 255, 0]
        test_stereo_right = [0, 255, 255, 0]

        binary_data = [(test_sick_back, sensor_data_dir / 'SICK_back'),
                       (test_sick_middle, sensor_data_dir / 'SICK_middle'),
                       (test_velodyne_left, sensor_data_dir / 'VLP_left'),
                       (test_velodyne_right, sensor_data_dir / 'VLP_right')
                       ]
        png_data = [(test_stereo_left, test_dataset_dir / 'image' / 'stereo_left'),
                    (test_stereo_right, test_dataset_dir / 'image' / 'stereo_right'),]

        csv_data = [(test_imu, sensor_data_dir / 'xsens_imu.csv'),
                    (test_fog, sensor_data_dir / 'fog.csv'),
                    (test_gps, sensor_data_dir / 'gps.csv'),
                    (test_vrs_gps, sensor_data_dir / 'vrs_gps.csv'),
                    (test_altimeter, sensor_data_dir / 'altimeter.csv'),
                    (test_encoder, sensor_data_dir / 'encoder.csv'),]

        for element, path in binary_data:
            self.to_binary_file(element, path / '1234.bin')

        for element, path in csv_data:
            self.to_csv_file(element, path)

        for element, path in png_data:
            self.to_png_file(element, path / '1234.png')

    def modify_default_config(self,) -> None:
        """
        1) rename to original
        2) copy data
        3) create with default name and insert copied data
        4) run test
        5) rename original to default name
        """
        original_config_path = TestDataFactory.DEFAULT_DATAMANAGER_CONFIG_PATH
        original_config_path.rename(
            TestDataFactory.MODIFIED_DATAMANAGER_CONFIG_PATH)

        test_dataset_dir = TestDataFactory.CURRENT_DIR / "test_data"
        test_params = {"data":
                       {
                           "dataset_type": "kaist",
                           "dataset_directory":  test_dataset_dir.as_posix()}
                       }

        with open(original_config_path, 'w') as outfile:
            safe_dump(test_params, outfile)
