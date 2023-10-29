import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Type

from numpy import ones, asarray
import numpy.typing as npt
import numpy as np
from cv2 import imwrite
from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module

from configs.sensors.base_sensor_parameters import ParameterConfig


from slam.data_manager.factory.readers.element_factory import (
    Element, Measurement)
from slam.data_manager.factory.readers.kaist.data_classes import (
    BinaryDataLocation, CsvDataLocation, StereoImgDataLocation)
from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, Altimeter, Gps, Sensor,
    VrsGps, Lidar2D, Lidar3D, StereoCamera)

from .config import TEST_DATA_DIR, SENSOR_CONFIG_NAME, CONFIG_MODULE_DIR


@dataclass
class SensorNamePath:
    name: str
    file_path: Path


@dataclass
class SensorElementPair:
    sensor: Type[Sensor]
    element: Element


class DataFactory:
    cs = ConfigStore.instance()
    cs.store(name=SENSOR_CONFIG_NAME, node=ParameterConfig)
    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        params = compose(config_name=SENSOR_CONFIG_NAME)

    CALIBRATION_DATA_DIR: Path = TEST_DATA_DIR / 'calibration'
    SENSOR_DATA_DIR: Path = TEST_DATA_DIR / 'sensor_data'
    IMAGE_DATA_DIR: Path = TEST_DATA_DIR / 'image'
    DATA_STAMP_FILE: Path = SENSOR_DATA_DIR / "data_stamp.csv"

    IMAGE_FILE_EXTENSION = '.png'
    BINARY_FILE_EXTENSION = '.bin'

    SICK_BACK_DIR: Path = Path('SICK_back')
    SICK_MIDDLE_DIR: Path = Path('SICK_middle')
    VLP_LEFT_DIR: Path = Path('VLP_left')
    VLP_RIGHT_DIR: Path = Path('VLP_right')
    STEREO_LEFT_DIR: Path = Path('stereo_left')
    STEREO_RIGHT_DIR: Path = Path('stereo_right')

    imu = SensorNamePath('imu', Path('xsens_imu.csv'),)
    fog = SensorNamePath('fog', Path('fog.csv'))
    encoder = SensorNamePath('encoder', Path('encoder.csv'))
    altimeter = SensorNamePath('altimeter', Path('altimeter.csv'))
    gps = SensorNamePath('gps', Path('gps.csv'))
    vrs_gps = SensorNamePath('vrs', Path('vrs_gps.csv'))
    sick_back = SensorNamePath('sick_back', Path('SICK_back_stamp.csv'))
    sick_middle = SensorNamePath('sick_middle', Path('SICK_middle_stamp.csv'))
    velodyne_left = SensorNamePath('velodyne_left', Path('VLP_left_stamp.csv'))
    velodyne_right = SensorNamePath(
        'velodyne_right', Path('VLP_right_stamp.csv'))
    stereo = SensorNamePath('stereo', Path('stereo_stamp.csv'))

    # data_stamp.csv file content. The order of the measurements.
    data_stamp = [
        [1, encoder.name],
        [2, sick_back.name],
        [3, imu.name],
        [4, fog.name],
        [5, sick_middle.name],
        [6, gps.name],
        [7, vrs_gps.name],
        [8, altimeter.name],
        [9, altimeter.name],
        [10, imu.name],
        [11, encoder.name],
        [12, sick_back.name],
        [13, gps.name],
        [14, sick_middle.name],
        [15, velodyne_left.name],
        [16, velodyne_right.name],
        [17, velodyne_left.name],
        [18, vrs_gps.name],
        [19, stereo.name],
        [20, velodyne_right.name],
        [21, fog.name],
        [22, stereo.name],
    ]

    # raw measurements
    z_encoder_1 = (1, 1.0, 1.0, 1.0)
    z_sick_back_1 = (2, 1.0, 1.0, 1.0)
    z_imu_1 = (3, 1.0, 1.0, 1.0)
    z_fog_1 = (4, 1.0, 1.0, 1.0)
    z_sick_middle_1 = (5, 1.0, 1.0, 1.0)
    z_gps_1 = (6, 1.0, 1.0, 1.0)
    z_vrs_gps_1 = (7, 1.0, 1.0, 1.0)
    z_altimeter_1 = (8, 1.0, 1.0, 1.0)
    z_altimeter_2 = (9, 1.0, 1.0, 1.0)
    z_imu_2 = (10, 1.0, 1.0, 1.0)
    z_encoder_2 = (11, 1.0, 1.0, 1.0)
    z_sick_back_2 = (12, 1.0, 1.0, 1.0)
    z_gps_2 = (13, 1.0, 1.0, 1.0)
    z_sick_middle_2 = (14, 1.0, 1.0, 1.0)
    z_velodyne_left_1 = (15, 1.0, 1.0, 1.0)
    z_velodyne_right_1 = (16, 1.0, 1.0, 1.0)
    z_velodyne_left_2 = (17, 1.0, 1.0, 1.0)
    z_vrs_gps_2 = (18, 1.0, 1.0, 1.0)
    z_stereo_left_1 = (19, tuple(ones(shape=(2, 2, 3))))
    z_stereo_right_1 = (19, tuple(ones(shape=(2, 2, 3))))
    z_velodyne_right_2 = (20, 1.0, 1.0, 1.0)
    z_fog_2 = (21, 1.0, 1.0, 1.0)
    z_stereo_left_2 = (22, tuple(ones(shape=(2, 2, 3))))
    z_stereo_right_2 = (22, tuple(ones(shape=(2, 2, 3))))

    binary_data = [(z_sick_back_1[1:],
                    SENSOR_DATA_DIR / SICK_BACK_DIR / str(z_sick_back_1[0])),
                   (z_sick_back_2[1:],
                    SENSOR_DATA_DIR / SICK_BACK_DIR / str(z_sick_back_2[0])),
                   (z_sick_middle_1[1:],
                    SENSOR_DATA_DIR / SICK_MIDDLE_DIR / str(z_sick_middle_1[0])),
                   (z_sick_middle_2[1:],
                    SENSOR_DATA_DIR / SICK_MIDDLE_DIR / str(z_sick_middle_2[0])),
                   (z_velodyne_left_1[1:],
                    SENSOR_DATA_DIR / VLP_LEFT_DIR / str(z_velodyne_left_1[0])),
                   (z_velodyne_left_2[1:],
                    SENSOR_DATA_DIR / VLP_LEFT_DIR / str(z_velodyne_left_2[0])),
                   (z_velodyne_right_1[1:],
                    SENSOR_DATA_DIR / VLP_RIGHT_DIR / str(z_velodyne_right_1[0])),
                   (z_velodyne_right_2[1:],
                    SENSOR_DATA_DIR / VLP_RIGHT_DIR / str(z_velodyne_right_2[0]))]

    png_data = [(z_stereo_left_1,
                 IMAGE_DATA_DIR / STEREO_LEFT_DIR / str(z_stereo_left_1[0])),
                (z_stereo_left_2,
                 IMAGE_DATA_DIR / STEREO_LEFT_DIR / str(z_stereo_left_2[0])),
                (z_stereo_right_1,
                 IMAGE_DATA_DIR / STEREO_RIGHT_DIR / str(z_stereo_right_1[0])),
                (z_stereo_right_2,
                 IMAGE_DATA_DIR / STEREO_RIGHT_DIR / str(z_stereo_right_2[0])),]

    csv_data = [(z_imu_1, SENSOR_DATA_DIR / imu.file_path),
                (z_imu_2, SENSOR_DATA_DIR / imu.file_path),
                (z_fog_1, SENSOR_DATA_DIR / fog.file_path),
                (z_fog_2, SENSOR_DATA_DIR / fog.file_path),
                (z_gps_1, SENSOR_DATA_DIR / gps.file_path),
                (z_gps_2, SENSOR_DATA_DIR / gps.file_path),
                (z_vrs_gps_1, SENSOR_DATA_DIR / vrs_gps.file_path),
                (z_vrs_gps_2, SENSOR_DATA_DIR / vrs_gps.file_path),
                (z_altimeter_1, SENSOR_DATA_DIR / altimeter.file_path),
                (z_altimeter_2, SENSOR_DATA_DIR / altimeter.file_path),
                (z_encoder_1, SENSOR_DATA_DIR / encoder.file_path),
                (z_encoder_2, SENSOR_DATA_DIR / encoder.file_path),]

    stamp_files = [([z_sick_back_1[0]],
                    SENSOR_DATA_DIR / sick_back.file_path),
                   ([z_sick_back_2[0]],
                    SENSOR_DATA_DIR / sick_back.file_path),
                   ([z_sick_middle_1[0]],
                    SENSOR_DATA_DIR / sick_middle.file_path),
                   ([z_sick_middle_2[0]],
                    SENSOR_DATA_DIR / sick_middle.file_path),
                   ([z_velodyne_left_1[0]],
                    SENSOR_DATA_DIR / velodyne_left.file_path),
                   ([z_velodyne_left_2[0]],
                    SENSOR_DATA_DIR / velodyne_left.file_path),
                   ([z_velodyne_right_1[0]],
                    SENSOR_DATA_DIR / velodyne_right.file_path),
                   ([z_velodyne_right_2[0]],
                    SENSOR_DATA_DIR / velodyne_right.file_path),
                   ([z_stereo_left_1[0]],
                    SENSOR_DATA_DIR / stereo.file_path),
                   ([z_stereo_left_2[0]],
                    SENSOR_DATA_DIR / stereo.file_path)]

    el1 = Element(
        timestamp=z_encoder_1[0],
        measurement=Measurement(
            sensor=Encoder(encoder.name, params),
            values=tuple(str(i) for i in z_encoder_1[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / encoder.file_path,
            position=0))

    el2 = Element(
        timestamp=z_sick_back_1[0],
        measurement=Measurement(
            sensor=Lidar2D(sick_back.name, params),
            values=z_sick_back_1[1:]),
        location=BinaryDataLocation(
            file=(SENSOR_DATA_DIR / SICK_BACK_DIR / str(z_sick_back_1[0])).with_suffix(BINARY_FILE_EXTENSION)))

    el3 = Element(
        timestamp=z_imu_1[0],
        measurement=Measurement(
            sensor=Imu(imu.name, params),
            values=tuple(str(i) for i in z_imu_1[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / imu.file_path,
            position=0))

    el4 = Element(
        timestamp=z_fog_1[0],
        measurement=Measurement(
            sensor=Fog(fog.name, params),
            values=tuple(str(i) for i in z_fog_1[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / fog.file_path,
            position=0))

    el5 = Element(
        timestamp=z_sick_middle_1[0],
        measurement=Measurement(
            sensor=Lidar2D(sick_middle.name, params),
            values=z_sick_middle_1[1:]),
        location=BinaryDataLocation(
            file=(SENSOR_DATA_DIR / SICK_MIDDLE_DIR / str(z_sick_middle_1[0])).with_suffix(BINARY_FILE_EXTENSION)))

    el6 = Element(
        timestamp=z_gps_1[0],
        measurement=Measurement(
            sensor=Gps(gps.name, params),
            values=tuple(str(i) for i in z_gps_1[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / gps.file_path,
            position=0))

    el7 = Element(
        timestamp=z_vrs_gps_1[0],
        measurement=Measurement(
            sensor=VrsGps(vrs_gps.name, params),
            values=tuple(str(i) for i in z_vrs_gps_1[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / vrs_gps.file_path,
            position=0))

    el8 = Element(
        timestamp=z_altimeter_1[0],
        measurement=Measurement(
            sensor=Altimeter(altimeter.name, params),
            values=tuple(str(i) for i in z_altimeter_1[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / altimeter.file_path,
            position=0))

    el9 = Element(
        timestamp=z_altimeter_2[0],
        measurement=Measurement(
            sensor=Altimeter(altimeter.name, params),
            values=tuple(str(i) for i in z_altimeter_2[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / altimeter.file_path,
            position=1))

    el10 = Element(
        timestamp=z_imu_2[0],
        measurement=Measurement(
            sensor=Imu(imu.name, params),
            values=tuple(str(i) for i in z_imu_2[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / imu.file_path,
            position=1))

    el11 = Element(
        timestamp=z_encoder_2[0],
        measurement=Measurement(
            sensor=Encoder(encoder.name, params),
            values=tuple(str(i) for i in z_encoder_2[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / encoder.file_path,
            position=1))

    el12 = Element(
        timestamp=z_sick_back_2[0],
        measurement=Measurement(
            sensor=Lidar2D(sick_back.name, params),
            values=z_sick_back_2[1:]),
        location=BinaryDataLocation(
            file=(SENSOR_DATA_DIR / SICK_BACK_DIR / str(z_sick_back_2[0])).with_suffix(BINARY_FILE_EXTENSION)))

    el13 = Element(
        timestamp=z_gps_2[0],
        measurement=Measurement(
            sensor=Gps(gps.name, params),
            values=tuple(str(i) for i in z_gps_2[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / gps.file_path,
            position=1))

    el14 = Element(
        timestamp=z_sick_middle_2[0],
        measurement=Measurement(
            sensor=Lidar2D(sick_middle.name, params),
            values=z_sick_middle_2[1:]),
        location=BinaryDataLocation(
            file=(SENSOR_DATA_DIR / SICK_MIDDLE_DIR / str(z_sick_middle_2[0])).with_suffix(BINARY_FILE_EXTENSION)))

    el15 = Element(
        timestamp=z_velodyne_left_1[0],
        measurement=Measurement(
            sensor=Lidar3D(velodyne_left.name, params),
            values=z_velodyne_left_1[1:]),
        location=BinaryDataLocation(
            file=(SENSOR_DATA_DIR / VLP_LEFT_DIR / str(z_velodyne_left_1[0])).with_suffix(BINARY_FILE_EXTENSION)))

    el16 = Element(
        timestamp=z_velodyne_right_1[0],
        measurement=Measurement(
            sensor=Lidar3D(velodyne_right.name, params),
            values=z_velodyne_right_1[1:]),
        location=BinaryDataLocation(
            file=(SENSOR_DATA_DIR / VLP_RIGHT_DIR / str(z_velodyne_right_1[0])).with_suffix(BINARY_FILE_EXTENSION)))

    el17 = Element(
        timestamp=z_velodyne_left_2[0],
        measurement=Measurement(
            sensor=Lidar3D(velodyne_left.name, params),
            values=z_velodyne_left_2[1:]),
        location=BinaryDataLocation(
            file=(SENSOR_DATA_DIR / VLP_LEFT_DIR / str(z_velodyne_left_2[0])).with_suffix(BINARY_FILE_EXTENSION)))

    el18 = Element(
        timestamp=z_vrs_gps_2[0],
        measurement=Measurement(
            sensor=VrsGps(vrs_gps.name, params),
            values=tuple(str(i) for i in z_vrs_gps_2[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / vrs_gps.file_path,
            position=1))

    el19 = Element(
        timestamp=z_stereo_left_1[0],
        measurement=Measurement(
            sensor=StereoCamera(stereo.name, params),
            values=(z_stereo_left_1[1:],
                    z_stereo_right_1[1:])),
        location=StereoImgDataLocation(
            files=((IMAGE_DATA_DIR / STEREO_LEFT_DIR / str(z_stereo_left_1[0])).with_suffix(IMAGE_FILE_EXTENSION),
                   (IMAGE_DATA_DIR / STEREO_RIGHT_DIR / str(z_stereo_right_1[0])).with_suffix(IMAGE_FILE_EXTENSION))))

    el20 = Element(
        timestamp=z_velodyne_right_2[0],
        measurement=Measurement(
            sensor=Lidar3D(velodyne_right.name, params),
            values=z_velodyne_right_2[1:]),
        location=BinaryDataLocation(
            file=(SENSOR_DATA_DIR / VLP_RIGHT_DIR / str(z_velodyne_right_2[0])).with_suffix(BINARY_FILE_EXTENSION)))

    el21 = Element(
        timestamp=z_fog_2[0],
        measurement=Measurement(
            sensor=Fog(fog.name, params),
            values=tuple(str(i) for i in z_fog_2[1:])),
        location=CsvDataLocation(
            file=SENSOR_DATA_DIR / fog.file_path,
            position=1))

    el22 = Element(
        timestamp=z_stereo_left_2[0],
        measurement=Measurement(
            sensor=StereoCamera(stereo.name, params),
            values=(z_stereo_left_2[1:],
                    z_stereo_right_2[1:])),
        location=StereoImgDataLocation(
            files=((IMAGE_DATA_DIR / STEREO_LEFT_DIR / str(z_stereo_left_2[0])).with_suffix(IMAGE_FILE_EXTENSION),
                   (IMAGE_DATA_DIR / STEREO_RIGHT_DIR / str(z_stereo_right_2[0])).with_suffix(IMAGE_FILE_EXTENSION))))

    elements: list[Element] = [el1, el2, el3, el4, el5, el6, el7,
                               el8, el9, el10, el11, el12, el13,
                               el14, el15, el16, el17, el18, el19,
                               el20, el21, el22]

    sensor_element_pairs = [
        SensorElementPair(
            Encoder(encoder.name, params),
            el1),
        SensorElementPair(
            Encoder(encoder.name, params),
            el11),
        SensorElementPair(
            Lidar2D(sick_back.name, params),
            el2),
        SensorElementPair(
            Lidar2D(sick_back.name, params),
            el12),
        SensorElementPair(
            Imu(imu.name, params),
            el3,),
        SensorElementPair(
            Imu(imu.name, params),
            el10),
        SensorElementPair(
            Fog(fog.name, params),
            el4,),
        SensorElementPair(
            Fog(fog.name, params),
            el21),
        SensorElementPair(
            Lidar2D(sick_middle.name, params),
            el5),
        SensorElementPair(
            Lidar2D(sick_middle.name, params),
            el14),
        SensorElementPair(
            Gps(gps.name, params),
            el6),
        SensorElementPair(
            Gps(gps.name, params),
            el13),
        SensorElementPair(
            VrsGps(vrs_gps.name, params),
            el7),
        SensorElementPair(
            VrsGps(vrs_gps.name, params),
            el18),
        SensorElementPair(
            Altimeter(altimeter.name, params),
            el8),
        SensorElementPair(
            Altimeter(altimeter.name, params),
            el9),
        SensorElementPair(
            Lidar3D(velodyne_left.name, params),
            el15),
        SensorElementPair(
            Lidar3D(velodyne_left.name, params),
            el17),
        SensorElementPair(
            Lidar3D(velodyne_right.name, params),
            el16),
        SensorElementPair(
            Lidar3D(velodyne_right.name, params),
            el20),
        SensorElementPair(
            StereoCamera(stereo.name, params),
            el19),
        SensorElementPair(
            StereoCamera(stereo.name, params),
            el22)
    ]

    @classmethod
    def to_binary_file(cls, data: list[float], path: Path) -> None:
        """
        Writes data to a binary file with floating point representation (float32) 
        due to lidar measurements format in Kaist Urban Dataset.

        Args:
            data (list[float]): data to be written.
            path (Path): binary file path.
        """
        with open(path, 'wb') as output_file:
            numpy_array = np.asarray(data, dtype=np.float32)
            numpy_array.tofile(output_file)

    @classmethod
    def to_csv_file(cls, data: list[float | list[str]], path: Path, multilines: bool = False) -> None:
        """
        Writes data to a CSV file.

        Args:
            data (list[float  |  list[str]]): data to be written to a CSV file.
            path (Path): file path.
            multilines (bool, optional): If True: writes list[list[str]] to the file. Defaults to False.
        """
        with open(path, 'a', encoding='UTF8', newline='') as outfile:
            writer = csv.writer(outfile)
            if multilines:
                writer.writerows(data)
            else:
                writer.writerow(data)

    @classmethod
    def to_img_file(cls, data: npt.NDArray[np.float32], path: Path) -> None:
        img = asarray(data[1])
        imwrite(path.as_posix(), img)

    def generate_data(self,) -> None:
        """
        Creates Kaist Urban dataset directory structure and generates data.
        """

        TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

        Path.mkdir(self.CALIBRATION_DATA_DIR, parents=True, exist_ok=True)
        Path.mkdir(self.IMAGE_DATA_DIR, parents=True, exist_ok=True)
        Path.mkdir(self.SENSOR_DATA_DIR, parents=True, exist_ok=True)

        Path.mkdir(self.IMAGE_DATA_DIR / self.STEREO_LEFT_DIR,
                   parents=True, exist_ok=True)
        Path.mkdir(self.IMAGE_DATA_DIR / self.STEREO_RIGHT_DIR,
                   parents=True, exist_ok=True)

        Path.mkdir(self.SENSOR_DATA_DIR / self.SICK_BACK_DIR,
                   parents=True, exist_ok=True)
        Path.mkdir(self.SENSOR_DATA_DIR / self.SICK_MIDDLE_DIR,
                   parents=True, exist_ok=True)
        Path.mkdir(self.SENSOR_DATA_DIR / self.VLP_LEFT_DIR,
                   parents=True, exist_ok=True)
        Path.mkdir(self.SENSOR_DATA_DIR / self.VLP_RIGHT_DIR,
                   parents=True, exist_ok=True)

        self.to_csv_file(
            self.data_stamp, self.DATA_STAMP_FILE, multilines=True)

        for element, path in self.csv_data:
            self.to_csv_file(element, path)

        for element, path in self.stamp_files:
            self.to_csv_file(element, path)

        for element, path in self.binary_data:
            self.to_binary_file(
                element, path.with_suffix(self.BINARY_FILE_EXTENSION))

        for element, path in self.png_data:
            self.to_img_file(element, path.with_suffix(
                self.IMAGE_FILE_EXTENSION))
