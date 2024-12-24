"""Kaist Urban dataset-like data."""

from pathlib import Path
from typing import Any

from numpy import dtype, ndarray, ones, uint8
from PIL import Image

from phd.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from phd.moduslam.data_manager.batch_factory.readers.locations import (
    BinaryDataLocation,
    CsvDataLocation,
    StereoImagesLocation,
)
from phd.moduslam.sensors_factory.sensors import Sensor
from phd.tests_data_generators.kaist_dataset.structure import DatasetStructure


class Data:
    def __init__(self, directory: Path):
        self.dataset = DatasetStructure(dataset_directory=directory)

        imu_name = "imu"
        fog_name = "fog"
        encoder_name = "encoder"
        altimeter_name = "altimeter"
        gps_name = "gps"
        vrs_gps_name = "vrs"
        sick_back_name = "sick_back"
        sick_middle_name = "sick_middle"
        velodyne_left_name = "velodyne_left"
        velodyne_right_name = "velodyne_right"
        stereo_name = "stereo"

        self.imu = Sensor(imu_name)
        self.fog = Sensor(fog_name)
        self.encoder = Sensor(encoder_name)
        self.altimeter = Sensor(altimeter_name)
        self.gps = Sensor(gps_name)
        self.vrs_gps = Sensor(vrs_gps_name)
        self.sick_back = Sensor(sick_back_name)
        self.sick_middle = Sensor(sick_middle_name)
        self.velodyne_left = Sensor(velodyne_left_name)
        self.velodyne_right = Sensor(velodyne_right_name)
        self.stereo = Sensor(stereo_name)

        # sensor stamp files
        imu_file = self.dataset.imu_data_file
        fog_file = self.dataset.fog_data_file
        encoder_file = self.dataset.encoder_data_file
        altimeter_file = self.dataset.altimeter_data_file
        gps_file = self.dataset.gps_data_file
        vrs_gps_file = self.dataset.vrs_gps_data_file
        sick_back_file = self.dataset.lidar_2D_back_stamp_file
        sick_middle_file = self.dataset.lidar_2D_middle_stamp_file
        velodyne_left_file = self.dataset.lidar_3D_left_stamp_file
        velodyne_right_file = self.dataset.lidar_3D_right_stamp_file
        stereo_file = self.dataset.stereo_stamp_file

        self.data_stamp_file = self.dataset.data_stamp_file

        # data_stamp.csv file content. The order of the measurements.
        self.data_stamp: list[tuple[int, str]] = [
            (1, encoder_name),
            (2, sick_back_name),
            (3, imu_name),
            (4, fog_name),
            (5, sick_middle_name),
            (6, gps_name),
            (7, vrs_gps_name),
            (8, altimeter_name),
            (9, altimeter_name),
            (10, imu_name),
            (11, encoder_name),
            (12, sick_back_name),
            (13, gps_name),
            (14, sick_middle_name),
            (15, velodyne_left_name),
            (16, velodyne_right_name),
            (17, velodyne_left_name),
            (18, vrs_gps_name),
            (19, stereo_name),
            (20, velodyne_right_name),
            (21, fog_name),
            (22, stereo_name),
            (23, imu_name),
            (24, stereo_name),
            (25, sick_middle_name),
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

        self.binary_data: list[tuple[tuple[float, ...], Path]] = [
            (
                z_sick_back_1[1:],
                (self.dataset.lidar_2D_back_dir / str(z_sick_back_1[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
            (
                z_sick_back_2[1:],
                (self.dataset.lidar_2D_back_dir / str(z_sick_back_2[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
            (
                z_sick_middle_1[1:],
                (self.dataset.lidar_2D_middle_dir / str(z_sick_middle_1[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
            (
                z_sick_middle_2[1:],
                (self.dataset.lidar_2D_middle_dir / str(z_sick_middle_2[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
            (
                z_sick_middle_3[1:],
                (self.dataset.lidar_2D_middle_dir / str(z_sick_middle_3[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
            (
                z_velodyne_left_1[1:],
                (self.dataset.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
            (
                z_velodyne_left_2[1:],
                (self.dataset.lidar_3D_left_dir / str(z_velodyne_left_2[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
            (
                z_velodyne_right_1[1:],
                (self.dataset.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
            (
                z_velodyne_right_2[1:],
                (self.dataset.lidar_3D_right_dir / str(z_velodyne_right_2[0])).with_suffix(
                    self.dataset.binary_file_extension
                ),
            ),
        ]

        self.image_data: list[tuple[tuple[int, ndarray[Any, dtype]], Path]] = [
            (
                z_stereo_left_1,
                (self.dataset.stereo_left_data_dir / str(z_stereo_left_1[0])).with_suffix(
                    self.dataset.image_file_extension
                ),
            ),
            (
                z_stereo_left_2,
                (self.dataset.stereo_left_data_dir / str(z_stereo_left_2[0])).with_suffix(
                    self.dataset.image_file_extension
                ),
            ),
            (
                z_stereo_left_3,
                (self.dataset.stereo_left_data_dir / str(z_stereo_left_3[0])).with_suffix(
                    self.dataset.image_file_extension
                ),
            ),
            (
                z_stereo_right_1,
                (self.dataset.stereo_right_data_dir / str(z_stereo_right_1[0])).with_suffix(
                    self.dataset.image_file_extension
                ),
            ),
            (
                z_stereo_right_2,
                (self.dataset.stereo_right_data_dir / str(z_stereo_right_2[0])).with_suffix(
                    self.dataset.image_file_extension
                ),
            ),
            (
                z_stereo_right_3,
                (self.dataset.stereo_right_data_dir / str(z_stereo_right_3[0])).with_suffix(
                    self.dataset.image_file_extension
                ),
            ),
        ]

        self.csv_data: list[tuple[tuple[int | float, ...], Path]] = [
            (z_imu_1, imu_file),
            (z_imu_2, imu_file),
            (z_imu_3, imu_file),
            (z_fog_1, fog_file),
            (z_fog_2, fog_file),
            (z_gps_1, gps_file),
            (z_gps_2, gps_file),
            (z_vrs_gps_1, vrs_gps_file),
            (z_vrs_gps_2, vrs_gps_file),
            (z_altimeter_1, altimeter_file),
            (z_altimeter_2, altimeter_file),
            (z_encoder_1, encoder_file),
            (z_encoder_2, encoder_file),
        ]

        self.stamp_files: list[tuple[int, Path]] = [
            (z_sick_back_1[0], sick_back_file),
            (z_sick_back_2[0], sick_back_file),
            (z_sick_middle_1[0], sick_middle_file),
            (z_sick_middle_2[0], sick_middle_file),
            (z_sick_middle_3[0], sick_middle_file),
            (z_velodyne_left_1[0], velodyne_left_file),
            (z_velodyne_left_2[0], velodyne_left_file),
            (z_velodyne_right_1[0], velodyne_right_file),
            (z_velodyne_right_2[0], velodyne_right_file),
            (z_stereo_left_1[0], stereo_file),
            (z_stereo_left_2[0], stereo_file),
            (z_stereo_left_3[0], stereo_file),
        ]

        el1 = Element(
            timestamp=z_encoder_1[0],
            measurement=RawMeasurement(
                sensor=self.encoder, values=tuple(str(i) for i in z_encoder_1[1:])
            ),
            location=CsvDataLocation(file=encoder_file, position=1),
        )

        el2 = Element(
            timestamp=z_sick_back_1[0],
            measurement=RawMeasurement(sensor=self.sick_back, values=z_sick_back_1[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_2D_back_dir / str(z_sick_back_1[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        el3 = Element(
            timestamp=z_imu_1[0],
            measurement=RawMeasurement(sensor=self.imu, values=tuple(str(i) for i in z_imu_1[1:])),
            location=CsvDataLocation(file=imu_file, position=1),
        )

        el4 = Element(
            timestamp=z_fog_1[0],
            measurement=RawMeasurement(sensor=self.fog, values=tuple(str(i) for i in z_fog_1[1:])),
            location=CsvDataLocation(file=fog_file, position=1),
        )

        el5 = Element(
            timestamp=z_sick_middle_1[0],
            measurement=RawMeasurement(sensor=self.sick_middle, values=z_sick_middle_1[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_2D_middle_dir / str(z_sick_middle_1[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        el6 = Element(
            timestamp=z_gps_1[0],
            measurement=RawMeasurement(sensor=self.gps, values=tuple(str(i) for i in z_gps_1[1:])),
            location=CsvDataLocation(file=gps_file, position=1),
        )

        el7 = Element(
            timestamp=z_vrs_gps_1[0],
            measurement=RawMeasurement(
                sensor=self.vrs_gps, values=tuple(str(i) for i in z_vrs_gps_1[1:])
            ),
            location=CsvDataLocation(file=vrs_gps_file, position=1),
        )

        el8 = Element(
            timestamp=z_altimeter_1[0],
            measurement=RawMeasurement(
                sensor=self.altimeter, values=tuple(str(i) for i in z_altimeter_1[1:])
            ),
            location=CsvDataLocation(file=altimeter_file, position=1),
        )

        el9 = Element(
            timestamp=z_altimeter_2[0],
            measurement=RawMeasurement(
                sensor=self.altimeter, values=tuple(str(i) for i in z_altimeter_2[1:])
            ),
            location=CsvDataLocation(file=altimeter_file, position=2),
        )

        el10 = Element(
            timestamp=z_imu_2[0],
            measurement=RawMeasurement(sensor=self.imu, values=tuple(str(i) for i in z_imu_2[1:])),
            location=CsvDataLocation(file=imu_file, position=2),
        )

        el11 = Element(
            timestamp=z_encoder_2[0],
            measurement=RawMeasurement(
                sensor=self.encoder, values=tuple(str(i) for i in z_encoder_2[1:])
            ),
            location=CsvDataLocation(file=encoder_file, position=2),
        )

        el12 = Element(
            timestamp=z_sick_back_2[0],
            measurement=RawMeasurement(sensor=self.sick_back, values=z_sick_back_2[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_2D_back_dir / str(z_sick_back_2[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        el13 = Element(
            timestamp=z_gps_2[0],
            measurement=RawMeasurement(sensor=self.gps, values=tuple(str(i) for i in z_gps_2[1:])),
            location=CsvDataLocation(file=gps_file, position=2),
        )

        el14 = Element(
            timestamp=z_sick_middle_2[0],
            measurement=RawMeasurement(sensor=self.sick_middle, values=z_sick_middle_2[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_2D_middle_dir / str(z_sick_middle_2[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        el15 = Element(
            timestamp=z_velodyne_left_1[0],
            measurement=RawMeasurement(sensor=self.velodyne_left, values=z_velodyne_left_1[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        el16 = Element(
            timestamp=z_velodyne_right_1[0],
            measurement=RawMeasurement(sensor=self.velodyne_right, values=z_velodyne_right_1[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        el17 = Element(
            timestamp=z_velodyne_left_2[0],
            measurement=RawMeasurement(sensor=self.velodyne_left, values=z_velodyne_left_2[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_3D_left_dir / str(z_velodyne_left_2[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        el18 = Element(
            timestamp=z_vrs_gps_2[0],
            measurement=RawMeasurement(
                sensor=self.vrs_gps, values=tuple(str(i) for i in z_vrs_gps_2[1:])
            ),
            location=CsvDataLocation(file=vrs_gps_file, position=2),
        )

        el19 = Element(
            timestamp=z_stereo_left_1[0],
            measurement=RawMeasurement(
                sensor=self.stereo,
                values=(
                    Image.fromarray(z_stereo_left_1[1]),
                    Image.fromarray(z_stereo_right_1[1]),
                ),
            ),
            location=StereoImagesLocation(
                files=(
                    (self.dataset.stereo_left_data_dir / str(z_stereo_left_1[0])).with_suffix(
                        self.dataset.image_file_extension
                    ),
                    (self.dataset.stereo_right_data_dir / str(z_stereo_right_1[0])).with_suffix(
                        self.dataset.image_file_extension
                    ),
                )
            ),
        )

        el20 = Element(
            timestamp=z_velodyne_right_2[0],
            measurement=RawMeasurement(sensor=self.velodyne_right, values=z_velodyne_right_2[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_3D_right_dir / str(z_velodyne_right_2[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        el21 = Element(
            timestamp=z_fog_2[0],
            measurement=RawMeasurement(sensor=self.fog, values=tuple(str(i) for i in z_fog_2[1:])),
            location=CsvDataLocation(file=fog_file, position=2),
        )

        el22 = Element(
            timestamp=z_stereo_left_2[0],
            measurement=RawMeasurement(
                sensor=self.stereo,
                values=(
                    Image.fromarray(z_stereo_left_2[1]),
                    Image.fromarray(z_stereo_right_2[1]),
                ),
            ),
            location=StereoImagesLocation(
                files=(
                    (self.dataset.stereo_left_data_dir / str(z_stereo_left_2[0])).with_suffix(
                        self.dataset.image_file_extension
                    ),
                    (self.dataset.stereo_right_data_dir / str(z_stereo_right_2[0])).with_suffix(
                        self.dataset.image_file_extension
                    ),
                )
            ),
        )

        el23 = Element(
            timestamp=z_imu_3[0],
            measurement=RawMeasurement(sensor=self.imu, values=tuple(str(i) for i in z_imu_3[1:])),
            location=CsvDataLocation(file=imu_file, position=3),
        )

        el24 = Element(
            timestamp=z_stereo_left_3[0],
            measurement=RawMeasurement(
                sensor=self.stereo,
                values=(
                    Image.fromarray(z_stereo_left_3[1]),
                    Image.fromarray(z_stereo_right_3[1]),
                ),
            ),
            location=StereoImagesLocation(
                files=(
                    (self.dataset.stereo_left_data_dir / str(z_stereo_left_3[0])).with_suffix(
                        self.dataset.image_file_extension
                    ),
                    (self.dataset.stereo_right_data_dir / str(z_stereo_right_3[0])).with_suffix(
                        self.dataset.image_file_extension
                    ),
                )
            ),
        )

        el25 = Element(
            timestamp=z_sick_middle_3[0],
            measurement=RawMeasurement(sensor=self.sick_middle, values=z_sick_middle_3[1:]),
            location=BinaryDataLocation(
                file=(self.dataset.lidar_2D_middle_dir / str(z_sick_middle_3[0])).with_suffix(
                    self.dataset.binary_file_extension
                )
            ),
        )

        self.elements: list[Element] = [
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
