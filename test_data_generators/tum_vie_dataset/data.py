"""Test data for the TUM VIE dataset.

left_images = 3 right_images = 3 imu = 30
"""

from pathlib import Path

import PIL
from PIL.Image import Image

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.directory_iterator import (
    DirectoryIterator,
)
from moduslam.data_manager.batch_factory.readers.locations import (
    CsvDataLocation,
    StereoImagesLocation,
)
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from moduslam.utils.auxiliary_methods import microsec2nanosec


class Data:
    def __init__(self, dataset_cfg: TumVieConfig):

        imu_name = dataset_cfg.imu_name
        stereo_name = dataset_cfg.stereo_name
        imu_file = dataset_cfg.directory / dataset_cfg.csv_files[imu_name]
        stereo_timestamps_file = dataset_cfg.directory / dataset_cfg.csv_files[stereo_name]
        left_images_dir = dataset_cfg.directory / dataset_cfg.stereo_data_dirs[0]
        right_images_dir = dataset_cfg.directory / dataset_cfg.stereo_data_dirs[1]

        self._imu_data = self.get_imu_data(imu_file)
        self._stereo_data = self.get_stereo_data(
            stereo_timestamps_file, left_images_dir, right_images_dir
        )

        self.imu = Sensor(SensorConfig(name=imu_name))
        self.stereo = Sensor(SensorConfig(name=stereo_name))

        imu_elements = self.create_imu_elements(self.imu, imu_file, self._imu_data)
        stereo_elements = self.create_stereo_elements(self.stereo, self._stereo_data)
        self.elements = imu_elements + stereo_elements
        self.elements.sort(key=lambda x: x.timestamp)

    @staticmethod
    def create_imu_elements(
        sensor: Sensor, file: Path, measurements: list[tuple[int, tuple[str, ...]]]
    ) -> list[Element]:
        """Creates elements with IMU data.

        Args:
            sensor: The IMU sensor.

            file: The path to the IMU file.

            measurements: The IMU data.

        Returns:
            list of elements with the IMU data.
        """
        elements: list[Element] = []

        for i, (timestamp, data) in enumerate(measurements):
            m = RawMeasurement(sensor, data)
            loc = CsvDataLocation(file=file, position=i + 1)
            el = Element(timestamp, m, loc)
            elements.append(el)
        return elements

    @staticmethod
    def create_stereo_elements(
        sensor: Sensor, measurements: list[tuple[int, Path, Path]]
    ) -> list[Element]:
        """Creates elements with stereo data.

        Args:
            sensor: The stereo camera sensor.

            measurements: The stereo data.

        Returns:
            list of elements with the stereo data.
        """

        elements: list[Element] = []
        for timestamp, left_image_file, right_image_file in measurements:
            left_image = PIL.Image.open(left_image_file)
            right_image = PIL.Image.open(right_image_file)
            m = RawMeasurement(sensor, (left_image, right_image))
            loc = StereoImagesLocation(files=(left_image_file, right_image_file))
            el = Element(timestamp, m, loc)
            elements.append(el)
        return elements

    @staticmethod
    def get_imu_data(imu_file: Path) -> list[tuple[int, tuple[str, ...]]]:
        """Reads the IMU data from the file.

        Args:
            imu_file (Path): The path to the IMU file.

        Returns:
            list of tuples with the timestamp and IMU data.
        """
        measurements: list[tuple[int, tuple[str, ...]]] = []

        with open(imu_file, "r") as f:
            next(f)  # skip header
            for line in f:
                line = line.strip()
                data = line.split()
                timestamp = microsec2nanosec(data[0])
                tuple_data = tuple(data[1:])
                measurements.append((timestamp, tuple_data))

        return measurements

    @staticmethod
    def get_stereo_data(
        timestamps_file: Path, left_images_dir: Path, right_images_dir: Path
    ) -> list[tuple[int, Path, Path]]:
        """Reads the stereo data from the files.

        Args:
            timestamps_file: path to the timestamps file.

            left_images_dir: path to the left images` directory.

            right_images_dir: path to the right images` directory.

        Returns:
            list of tuples with the timestamp and left, right image paths.
        """

        left_images_iter = DirectoryIterator(left_images_dir, ".jpg")
        right_images_iter = DirectoryIterator(right_images_dir, ".jpg")
        measurements: list[tuple[int, Path, Path]] = []

        with open(timestamps_file, "r") as f:
            next(f)  # skip header
            for line in f:
                line = line.strip()
                data = line.split()
                timestamp = microsec2nanosec(data[0])

                left_image_file = next(left_images_iter)
                right_image_file = next(right_images_iter)
                measurements.append((timestamp, left_image_file, right_image_file))

        return measurements
