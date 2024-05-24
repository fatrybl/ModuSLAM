"""Kaist Urban dataset -like data."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from numpy import dtype, ndarray, ones, uint8
from PIL import Image

from moduslam.data_manager.factory.element import Element, RawMeasurement
from moduslam.data_manager.factory.locations import (
    BinaryDataLocation,
    CsvDataLocation,
    StereoImgDataLocation,
)
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from tests_data.kaist_urban_dataset.structure import DatasetStructure


@dataclass
class SensorNamePath:
    name: str
    file_path: Path


@dataclass
class SensorElementPair:
    sensor: Sensor
    element: Element


DATASET_DIR = Path(__file__).parent / "tmp/"

ds = DatasetStructure(dataset_directory=DATASET_DIR)


# sensor stamp files
imu = SensorNamePath("imu", ds.imu_data_file)
fog = SensorNamePath("fog", ds.fog_data_file)
encoder = SensorNamePath("encoder", ds.encoder_data_file)
altimeter = SensorNamePath("altimeter", ds.altimeter_data_file)
gps = SensorNamePath("gps", ds.gps_data_file)
vrs_gps = SensorNamePath("vrs", ds.vrs_gps_data_file)
sick_back = SensorNamePath("sick_back", ds.lidar_2D_back_stamp_file)
sick_middle = SensorNamePath("sick_middle", ds.lidar_2D_middle_stamp_file)
velodyne_left = SensorNamePath("velodyne_left", ds.lidar_3D_left_stamp_file)
velodyne_right = SensorNamePath("velodyne_right", ds.lidar_3D_right_stamp_file)
stereo = SensorNamePath("stereo", ds.stereo_stamp_file)

imu_params = SensorConfig(name=imu.name)
fog_params = SensorConfig(name=fog.name)
encoder_params = SensorConfig(name=encoder.name)
altimeter_params = SensorConfig(name=altimeter.name)
gps_params = SensorConfig(name=gps.name)
vrs_gps_params = SensorConfig(name=vrs_gps.name)
sick_back_params = SensorConfig(name=sick_back.name)
sick_middle_params = SensorConfig(name=sick_middle.name)
velodyne_left_params = SensorConfig(name=velodyne_left.name)
velodyne_right_params = SensorConfig(name=velodyne_right.name)
stereo_params = SensorConfig(name=stereo.name)


sensor_factory_cfg = SensorFactoryConfig(
    sensors={
        imu.name: imu_params,
        fog.name: fog_params,
        encoder.name: encoder_params,
        altimeter.name: altimeter_params,
        gps.name: gps_params,
        vrs_gps.name: vrs_gps_params,
        sick_back.name: sick_back_params,
        sick_middle.name: sick_middle_params,
        velodyne_left.name: velodyne_left_params,
        velodyne_right.name: velodyne_right_params,
        stereo.name: stereo_params,
    }
)

# data_stamp.csv file content. The order of the measurements.
data_stamp: list[list[int | str]] = [
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
    [23, imu.name],
    [24, stereo.name],
    [25, sick_middle.name],
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
z_stereo_left_1 = (19, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_right_1 = (19, ones(shape=(2, 2, 3)).astype(uint8))
z_velodyne_right_2 = (20, 1.0, 1.0, 1.0)
z_fog_2 = (21, 1.0, 1.0, 1.0)
z_stereo_left_2 = (22, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_right_2 = (22, ones(shape=(2, 2, 3)).astype(uint8))
z_imu_3 = (23, 1.0, 1.0, 1.0)
z_stereo_left_3 = (24, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_right_3 = (24, ones(shape=(2, 2, 3)).astype(uint8))
z_sick_middle_3 = (25, 1.0, 1.0, 1.0)

binary_data: list[tuple[tuple[float, ...], Path]] = [
    (
        z_sick_back_1[1:],
        (ds.lidar_2D_back_dir / str(z_sick_back_1[0])).with_suffix(ds.binary_file_extension),
    ),
    (
        z_sick_back_2[1:],
        (ds.lidar_2D_back_dir / str(z_sick_back_2[0])).with_suffix(ds.binary_file_extension),
    ),
    (
        z_sick_middle_1[1:],
        (ds.lidar_2D_middle_dir / str(z_sick_middle_1[0])).with_suffix(ds.binary_file_extension),
    ),
    (
        z_sick_middle_2[1:],
        (ds.lidar_2D_middle_dir / str(z_sick_middle_2[0])).with_suffix(ds.binary_file_extension),
    ),
    (
        z_sick_middle_3[1:],
        (ds.lidar_2D_middle_dir / str(z_sick_middle_3[0])).with_suffix(ds.binary_file_extension),
    ),
    (
        z_velodyne_left_1[1:],
        (ds.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(ds.binary_file_extension),
    ),
    (
        z_velodyne_left_2[1:],
        (ds.lidar_3D_left_dir / str(z_velodyne_left_2[0])).with_suffix(ds.binary_file_extension),
    ),
    (
        z_velodyne_right_1[1:],
        (ds.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(ds.binary_file_extension),
    ),
    (
        z_velodyne_right_2[1:],
        (ds.lidar_3D_right_dir / str(z_velodyne_right_2[0])).with_suffix(ds.binary_file_extension),
    ),
]

image_data: list[tuple[tuple[int, ndarray[Any, dtype]], Path]] = [
    (
        z_stereo_left_1,
        (ds.stereo_left_data_dir / str(z_stereo_left_1[0])).with_suffix(ds.image_file_extension),
    ),
    (
        z_stereo_left_2,
        (ds.stereo_left_data_dir / str(z_stereo_left_2[0])).with_suffix(ds.image_file_extension),
    ),
    (
        z_stereo_left_3,
        (ds.stereo_left_data_dir / str(z_stereo_left_3[0])).with_suffix(ds.image_file_extension),
    ),
    (
        z_stereo_right_1,
        (ds.stereo_right_data_dir / str(z_stereo_right_1[0])).with_suffix(ds.image_file_extension),
    ),
    (
        z_stereo_right_2,
        (ds.stereo_right_data_dir / str(z_stereo_right_2[0])).with_suffix(ds.image_file_extension),
    ),
    (
        z_stereo_right_3,
        (ds.stereo_right_data_dir / str(z_stereo_right_3[0])).with_suffix(ds.image_file_extension),
    ),
]

csv_data: list[tuple[tuple[int | float, ...], Path]] = [
    (z_imu_1, imu.file_path),
    (z_imu_2, imu.file_path),
    (z_imu_3, imu.file_path),
    (z_fog_1, fog.file_path),
    (z_fog_2, fog.file_path),
    (z_gps_1, gps.file_path),
    (z_gps_2, gps.file_path),
    (z_vrs_gps_1, vrs_gps.file_path),
    (z_vrs_gps_2, vrs_gps.file_path),
    (z_altimeter_1, altimeter.file_path),
    (z_altimeter_2, altimeter.file_path),
    (z_encoder_1, encoder.file_path),
    (z_encoder_2, encoder.file_path),
]

stamp_files: list[tuple[int, Path]] = [
    (z_sick_back_1[0], sick_back.file_path),
    (z_sick_back_2[0], sick_back.file_path),
    (z_sick_middle_1[0], sick_middle.file_path),
    (z_sick_middle_2[0], sick_middle.file_path),
    (z_sick_middle_3[0], sick_middle.file_path),
    (z_velodyne_left_1[0], velodyne_left.file_path),
    (z_velodyne_left_2[0], velodyne_left.file_path),
    (z_velodyne_right_1[0], velodyne_right.file_path),
    (z_velodyne_right_2[0], velodyne_right.file_path),
    (z_stereo_left_1[0], stereo.file_path),
    (z_stereo_left_2[0], stereo.file_path),
    (z_stereo_left_3[0], stereo.file_path),
]

el1 = Element(
    timestamp=z_encoder_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(encoder_params),
        values=tuple(str(i) for i in z_encoder_1[1:]),
    ),
    location=CsvDataLocation(file=encoder.file_path, position=1),
)

el2 = Element(
    timestamp=z_sick_back_1[0],
    measurement=RawMeasurement(sensor=Sensor(sick_back_params), values=z_sick_back_1[1:]),
    location=BinaryDataLocation(
        file=(ds.lidar_2D_back_dir / str(z_sick_back_1[0])).with_suffix(ds.binary_file_extension)
    ),
)

el3 = Element(
    timestamp=z_imu_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(imu_params), values=tuple(str(i) for i in z_imu_1[1:])
    ),
    location=CsvDataLocation(file=imu.file_path, position=1),
)

el4 = Element(
    timestamp=z_fog_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(fog_params), values=tuple(str(i) for i in z_fog_1[1:])
    ),
    location=CsvDataLocation(file=fog.file_path, position=1),
)

el5 = Element(
    timestamp=z_sick_middle_1[0],
    measurement=RawMeasurement(sensor=Sensor(sick_middle_params), values=z_sick_middle_1[1:]),
    location=BinaryDataLocation(
        file=(ds.lidar_2D_middle_dir / str(z_sick_middle_1[0])).with_suffix(
            ds.binary_file_extension
        )
    ),
)

el6 = Element(
    timestamp=z_gps_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(gps_params), values=tuple(str(i) for i in z_gps_1[1:])
    ),
    location=CsvDataLocation(file=gps.file_path, position=1),
)

el7 = Element(
    timestamp=z_vrs_gps_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(vrs_gps_params),
        values=tuple(str(i) for i in z_vrs_gps_1[1:]),
    ),
    location=CsvDataLocation(file=vrs_gps.file_path, position=1),
)

el8 = Element(
    timestamp=z_altimeter_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(altimeter_params),
        values=tuple(str(i) for i in z_altimeter_1[1:]),
    ),
    location=CsvDataLocation(file=altimeter.file_path, position=1),
)

el9 = Element(
    timestamp=z_altimeter_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(altimeter_params),
        values=tuple(str(i) for i in z_altimeter_2[1:]),
    ),
    location=CsvDataLocation(file=altimeter.file_path, position=2),
)

el10 = Element(
    timestamp=z_imu_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(imu_params), values=tuple(str(i) for i in z_imu_2[1:])
    ),
    location=CsvDataLocation(file=imu.file_path, position=2),
)

el11 = Element(
    timestamp=z_encoder_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(encoder_params),
        values=tuple(str(i) for i in z_encoder_2[1:]),
    ),
    location=CsvDataLocation(file=encoder.file_path, position=2),
)

el12 = Element(
    timestamp=z_sick_back_2[0],
    measurement=RawMeasurement(sensor=Sensor(sick_back_params), values=z_sick_back_2[1:]),
    location=BinaryDataLocation(
        file=(ds.lidar_2D_back_dir / str(z_sick_back_2[0])).with_suffix(ds.binary_file_extension)
    ),
)

el13 = Element(
    timestamp=z_gps_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(gps_params), values=tuple(str(i) for i in z_gps_2[1:])
    ),
    location=CsvDataLocation(file=gps.file_path, position=2),
)

el14 = Element(
    timestamp=z_sick_middle_2[0],
    measurement=RawMeasurement(sensor=Sensor(sick_middle_params), values=z_sick_middle_2[1:]),
    location=BinaryDataLocation(
        file=(ds.lidar_2D_middle_dir / str(z_sick_middle_2[0])).with_suffix(
            ds.binary_file_extension
        )
    ),
)

el15 = Element(
    timestamp=z_velodyne_left_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(velodyne_left_params),
        values=z_velodyne_left_1[1:],
    ),
    location=BinaryDataLocation(
        file=(ds.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(
            ds.binary_file_extension
        )
    ),
)

el16 = Element(
    timestamp=z_velodyne_right_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(velodyne_right_params),
        values=z_velodyne_right_1[1:],
    ),
    location=BinaryDataLocation(
        file=(ds.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(
            ds.binary_file_extension
        )
    ),
)

el17 = Element(
    timestamp=z_velodyne_left_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(velodyne_left_params),
        values=z_velodyne_left_2[1:],
    ),
    location=BinaryDataLocation(
        file=(ds.lidar_3D_left_dir / str(z_velodyne_left_2[0])).with_suffix(
            ds.binary_file_extension
        )
    ),
)

el18 = Element(
    timestamp=z_vrs_gps_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(vrs_gps_params),
        values=tuple(str(i) for i in z_vrs_gps_2[1:]),
    ),
    location=CsvDataLocation(file=vrs_gps.file_path, position=2),
)

el19 = Element(
    timestamp=z_stereo_left_1[0],
    measurement=RawMeasurement(
        sensor=Sensor(stereo_params),
        values=(
            Image.fromarray(z_stereo_left_1[1]),
            Image.fromarray(z_stereo_right_1[1]),
        ),
    ),
    location=StereoImgDataLocation(
        files=(
            (ds.stereo_left_data_dir / str(z_stereo_left_1[0])).with_suffix(
                ds.image_file_extension
            ),
            (ds.stereo_right_data_dir / str(z_stereo_right_1[0])).with_suffix(
                ds.image_file_extension
            ),
        )
    ),
)

el20 = Element(
    timestamp=z_velodyne_right_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(velodyne_right_params),
        values=z_velodyne_right_2[1:],
    ),
    location=BinaryDataLocation(
        file=(ds.lidar_3D_right_dir / str(z_velodyne_right_2[0])).with_suffix(
            ds.binary_file_extension
        )
    ),
)

el21 = Element(
    timestamp=z_fog_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(fog_params), values=tuple(str(i) for i in z_fog_2[1:])
    ),
    location=CsvDataLocation(file=fog.file_path, position=2),
)

el22 = Element(
    timestamp=z_stereo_left_2[0],
    measurement=RawMeasurement(
        sensor=Sensor(stereo_params),
        values=(
            Image.fromarray(z_stereo_left_2[1]),
            Image.fromarray(z_stereo_right_2[1]),
        ),
    ),
    location=StereoImgDataLocation(
        files=(
            (ds.stereo_left_data_dir / str(z_stereo_left_2[0])).with_suffix(
                ds.image_file_extension
            ),
            (ds.stereo_right_data_dir / str(z_stereo_right_2[0])).with_suffix(
                ds.image_file_extension
            ),
        )
    ),
)

el23 = Element(
    timestamp=z_imu_3[0],
    measurement=RawMeasurement(
        sensor=Sensor(imu_params), values=tuple(str(i) for i in z_imu_3[1:])
    ),
    location=CsvDataLocation(file=imu.file_path, position=3),
)

el24 = Element(
    timestamp=z_stereo_left_3[0],
    measurement=RawMeasurement(
        sensor=Sensor(stereo_params),
        values=(
            Image.fromarray(z_stereo_left_3[1]),
            Image.fromarray(z_stereo_right_3[1]),
        ),
    ),
    location=StereoImgDataLocation(
        files=(
            (ds.stereo_left_data_dir / str(z_stereo_left_3[0])).with_suffix(
                ds.image_file_extension
            ),
            (ds.stereo_right_data_dir / str(z_stereo_right_3[0])).with_suffix(
                ds.image_file_extension
            ),
        )
    ),
)

el25 = Element(
    timestamp=z_sick_middle_3[0],
    measurement=RawMeasurement(sensor=Sensor(sick_middle_params), values=z_sick_middle_3[1:]),
    location=BinaryDataLocation(
        file=(ds.lidar_2D_middle_dir / str(z_sick_middle_3[0])).with_suffix(
            ds.binary_file_extension
        )
    ),
)


elements: list[Element] = [
    el1,
    el2,
    el3,
    el4,
    el5,
    el6,
    el7,
    el8,
    el9,
    el10,
    el11,
    el12,
    el13,
    el14,
    el15,
    el16,
    el17,
    el18,
    el19,
    el20,
    el21,
    el22,
    el23,
    el24,
    el25,
]
