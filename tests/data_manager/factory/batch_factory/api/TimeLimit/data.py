import itertools
from dataclasses import dataclass
from pathlib import Path

from hydra import compose, initialize_config_module
from hydra.core.config_store import ConfigStore
from numpy import ones, uint8
from PIL import Image

from configs.paths.kaist_dataset import KaistDatasetPathConfig
from configs.sensors.base_sensor_parameters import ParameterConfig
from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.kaist.data_classes import (
    BinaryDataLocation,
    CsvDataLocation,
    StereoImgDataLocation,
)
from slam.setup_manager.sensor_factory.sensors import (
    Altimeter,
    Encoder,
    Fog,
    Gps,
    Imu,
    Lidar2D,
    Lidar3D,
    StereoCamera,
    VrsGps,
)
from slam.utils.auxiliary_dataclasses import PeriodicData, TimeRange
from tests.data_manager.auxiliary_utils.kaist_data_factory import SensorNamePath
from tests.data_manager.factory.batch_factory.api.TimeLimit.config import DATASET_DIR
from tests.data_manager.factory.batch_factory.conftest import SENSOR_FACTORY_CONFIG_NAME

cs = ConfigStore.instance()
cs.store(name=SENSOR_FACTORY_CONFIG_NAME, node=ParameterConfig)
with initialize_config_module(config_module="tests.data_manager.factory.batch_factory.api.conf"):
    params = compose(config_name=SENSOR_FACTORY_CONFIG_NAME)


"""
each sensor request:
    1) start==stop: start of dataset
    2) start==stop: end of dataset
    3) start==stop: middle of dataset
    4) start!=stop: all elements in dataset
    5) start!=stop: some middle elements in dataset
    6) start!=stop: from start to middle of dataset
    7) start!=stop: from middle to end of dataset
    8) start!=stop: from start to pre-end of dataset
    9) start!=stop: from 2nd-start to end of dataset

    In total: 9*N cases, 9 - number of test cases per sensor, N - number of sensors.
"""


@dataclass(frozen=True)
class DatasetStructure:
    dataset_directory: Path = DATASET_DIR
    calibration_data_dir: Path = dataset_directory / KaistDatasetPathConfig.calibration_data_dir
    sensor_data_dir: Path = dataset_directory / KaistDatasetPathConfig.sensor_data_dir
    image_data_dir: Path = dataset_directory / KaistDatasetPathConfig.image_data_dir
    data_stamp: Path = dataset_directory / KaistDatasetPathConfig.data_stamp
    lidar_2D_back_dir: Path = dataset_directory / KaistDatasetPathConfig.lidar_2D_back_dir
    lidar_2D_middle_dir: Path = dataset_directory / KaistDatasetPathConfig.lidar_2D_middle_dir
    lidar_3D_left_dir: Path = dataset_directory / KaistDatasetPathConfig.lidar_3D_left_dir
    lidar_3D_right_dir: Path = dataset_directory / KaistDatasetPathConfig.lidar_3D_right_dir
    stereo_left_data_dir: Path = (
        dataset_directory / KaistDatasetPathConfig.image_data_dir / KaistDatasetPathConfig.stereo_left_data_dir
    )
    stereo_right_data_dir: Path = (
        dataset_directory / KaistDatasetPathConfig.image_data_dir / KaistDatasetPathConfig.stereo_right_data_dir
    )

    imu_data_file: Path = dataset_directory / KaistDatasetPathConfig.imu_data_file
    fog_data_file: Path = dataset_directory / KaistDatasetPathConfig.fog_data_file
    encoder_data_file: Path = dataset_directory / KaistDatasetPathConfig.encoder_data_file
    altimeter_data_file: Path = dataset_directory / KaistDatasetPathConfig.altimeter_data_file
    gps_data_file: Path = dataset_directory / KaistDatasetPathConfig.gps_data_file
    vrs_gps_data_file: Path = dataset_directory / KaistDatasetPathConfig.vrs_gps_data_file
    lidar_2D_back_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.lidar_2D_back_stamp_file
    lidar_2D_middle_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.lidar_2D_middle_stamp_file
    lidar_3D_left_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.lidar_3D_left_stamp_file
    lidar_3D_right_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.lidar_3D_right_stamp_file
    stereo_stamp_file: Path = dataset_directory / KaistDatasetPathConfig.stereo_stamp_file

    binary_file_extension: str = ".bin"
    image_file_extension: str = ".png"


# sensor stamp files
imu = SensorNamePath("imu", DatasetStructure.imu_data_file)
fog = SensorNamePath("fog", DatasetStructure.fog_data_file)
encoder = SensorNamePath("encoder", DatasetStructure.encoder_data_file)
altimeter = SensorNamePath("altimeter", DatasetStructure.altimeter_data_file)
gps = SensorNamePath("gps", DatasetStructure.gps_data_file)
vrs_gps = SensorNamePath("vrs", DatasetStructure.vrs_gps_data_file)
sick_back = SensorNamePath("sick_back", DatasetStructure.lidar_2D_back_stamp_file)
sick_middle = SensorNamePath("sick_middle", DatasetStructure.lidar_2D_middle_stamp_file)
velodyne_left = SensorNamePath("velodyne_left", DatasetStructure.lidar_3D_left_stamp_file)
velodyne_right = SensorNamePath("velodyne_right", DatasetStructure.lidar_3D_right_stamp_file)
stereo = SensorNamePath("stereo", DatasetStructure.stereo_stamp_file)

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

binary_data = [
    (
        z_sick_back_1[1:],
        (DatasetStructure.lidar_2D_back_dir / str(z_sick_back_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_sick_back_2[1:],
        (DatasetStructure.lidar_2D_back_dir / str(z_sick_back_2[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_sick_middle_1[1:],
        (DatasetStructure.lidar_2D_middle_dir / str(z_sick_middle_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_sick_middle_2[1:],
        (DatasetStructure.lidar_2D_middle_dir / str(z_sick_middle_2[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_sick_middle_3[1:],
        (DatasetStructure.lidar_2D_middle_dir / str(z_sick_middle_3[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_velodyne_left_1[1:],
        (DatasetStructure.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_velodyne_left_2[1:],
        (DatasetStructure.lidar_3D_left_dir / str(z_velodyne_left_2[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_velodyne_right_1[1:],
        (DatasetStructure.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_velodyne_right_2[1:],
        (DatasetStructure.lidar_3D_right_dir / str(z_velodyne_right_2[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
]

image_data = [
    (
        z_stereo_left_1,
        (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_1[0])).with_suffix(
            DatasetStructure.image_file_extension
        ),
    ),
    (
        z_stereo_left_2,
        (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_2[0])).with_suffix(
            DatasetStructure.image_file_extension
        ),
    ),
    (
        z_stereo_left_3,
        (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_3[0])).with_suffix(
            DatasetStructure.image_file_extension
        ),
    ),
    (
        z_stereo_right_1,
        (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_1[0])).with_suffix(
            DatasetStructure.image_file_extension
        ),
    ),
    (
        z_stereo_right_2,
        (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_2[0])).with_suffix(
            DatasetStructure.image_file_extension
        ),
    ),
    (
        z_stereo_right_3,
        (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_3[0])).with_suffix(
            DatasetStructure.image_file_extension
        ),
    ),
]

csv_data = [
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

stamp_files = [
    ([z_sick_back_1[0]], sick_back.file_path),
    ([z_sick_back_2[0]], sick_back.file_path),
    ([z_sick_middle_1[0]], sick_middle.file_path),
    ([z_sick_middle_2[0]], sick_middle.file_path),
    ([z_sick_middle_3[0]], sick_middle.file_path),
    ([z_velodyne_left_1[0]], velodyne_left.file_path),
    ([z_velodyne_left_2[0]], velodyne_left.file_path),
    ([z_velodyne_right_1[0]], velodyne_right.file_path),
    ([z_velodyne_right_2[0]], velodyne_right.file_path),
    ([z_stereo_left_1[0]], stereo.file_path),
    ([z_stereo_left_2[0]], stereo.file_path),
    ([z_stereo_left_3[0]], stereo.file_path),
]

el1 = Element(
    timestamp=z_encoder_1[0],
    measurement=Measurement(
        sensor=Encoder(encoder.name, params),
        values=tuple(str(i) for i in z_encoder_1[1:]),
    ),
    location=CsvDataLocation(file=encoder.file_path, position=0),
)

el2 = Element(
    timestamp=z_sick_back_1[0],
    measurement=Measurement(sensor=Lidar2D(sick_back.name, params), values=z_sick_back_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_back_dir / str(z_sick_back_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el3 = Element(
    timestamp=z_imu_1[0],
    measurement=Measurement(sensor=Imu(imu.name, params), values=tuple(str(i) for i in z_imu_1[1:])),
    location=CsvDataLocation(file=imu.file_path, position=0),
)

el4 = Element(
    timestamp=z_fog_1[0],
    measurement=Measurement(sensor=Fog(fog.name, params), values=tuple(str(i) for i in z_fog_1[1:])),
    location=CsvDataLocation(file=fog.file_path, position=0),
)

el5 = Element(
    timestamp=z_sick_middle_1[0],
    measurement=Measurement(sensor=Lidar2D(sick_middle.name, params), values=z_sick_middle_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_middle_dir / str(z_sick_middle_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el6 = Element(
    timestamp=z_gps_1[0],
    measurement=Measurement(sensor=Gps(gps.name, params), values=tuple(str(i) for i in z_gps_1[1:])),
    location=CsvDataLocation(file=gps.file_path, position=0),
)

el7 = Element(
    timestamp=z_vrs_gps_1[0],
    measurement=Measurement(
        sensor=VrsGps(vrs_gps.name, params),
        values=tuple(str(i) for i in z_vrs_gps_1[1:]),
    ),
    location=CsvDataLocation(file=vrs_gps.file_path, position=0),
)

el8 = Element(
    timestamp=z_altimeter_1[0],
    measurement=Measurement(
        sensor=Altimeter(altimeter.name, params),
        values=tuple(str(i) for i in z_altimeter_1[1:]),
    ),
    location=CsvDataLocation(file=altimeter.file_path, position=0),
)

el9 = Element(
    timestamp=z_altimeter_2[0],
    measurement=Measurement(
        sensor=Altimeter(altimeter.name, params),
        values=tuple(str(i) for i in z_altimeter_2[1:]),
    ),
    location=CsvDataLocation(file=altimeter.file_path, position=1),
)

el10 = Element(
    timestamp=z_imu_2[0],
    measurement=Measurement(sensor=Imu(imu.name, params), values=tuple(str(i) for i in z_imu_2[1:])),
    location=CsvDataLocation(file=imu.file_path, position=1),
)

el11 = Element(
    timestamp=z_encoder_2[0],
    measurement=Measurement(
        sensor=Encoder(encoder.name, params),
        values=tuple(str(i) for i in z_encoder_2[1:]),
    ),
    location=CsvDataLocation(file=encoder.file_path, position=1),
)

el12 = Element(
    timestamp=z_sick_back_2[0],
    measurement=Measurement(sensor=Lidar2D(sick_back.name, params), values=z_sick_back_2[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_back_dir / str(z_sick_back_2[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el13 = Element(
    timestamp=z_gps_2[0],
    measurement=Measurement(sensor=Gps(gps.name, params), values=tuple(str(i) for i in z_gps_2[1:])),
    location=CsvDataLocation(file=gps.file_path, position=1),
)

el14 = Element(
    timestamp=z_sick_middle_2[0],
    measurement=Measurement(sensor=Lidar2D(sick_middle.name, params), values=z_sick_middle_2[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_middle_dir / str(z_sick_middle_2[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el15 = Element(
    timestamp=z_velodyne_left_1[0],
    measurement=Measurement(sensor=Lidar3D(velodyne_left.name, params), values=z_velodyne_left_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el16 = Element(
    timestamp=z_velodyne_right_1[0],
    measurement=Measurement(sensor=Lidar3D(velodyne_right.name, params), values=z_velodyne_right_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el17 = Element(
    timestamp=z_velodyne_left_2[0],
    measurement=Measurement(sensor=Lidar3D(velodyne_left.name, params), values=z_velodyne_left_2[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_3D_left_dir / str(z_velodyne_left_2[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el18 = Element(
    timestamp=z_vrs_gps_2[0],
    measurement=Measurement(
        sensor=VrsGps(vrs_gps.name, params),
        values=tuple(str(i) for i in z_vrs_gps_2[1:]),
    ),
    location=CsvDataLocation(file=vrs_gps.file_path, position=1),
)

el19 = Element(
    timestamp=z_stereo_left_1[0],
    measurement=Measurement(
        sensor=StereoCamera(stereo.name, params),
        values=(
            Image.fromarray(z_stereo_left_1[1]),
            Image.fromarray(z_stereo_right_1[1]),
        ),
    ),
    location=StereoImgDataLocation(
        files=(
            (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_1[0])).with_suffix(
                DatasetStructure.image_file_extension
            ),
            (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_1[0])).with_suffix(
                DatasetStructure.image_file_extension
            ),
        )
    ),
)

el20 = Element(
    timestamp=z_velodyne_right_2[0],
    measurement=Measurement(sensor=Lidar3D(velodyne_right.name, params), values=z_velodyne_right_2[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_3D_right_dir / str(z_velodyne_right_2[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el21 = Element(
    timestamp=z_fog_2[0],
    measurement=Measurement(sensor=Fog(fog.name, params), values=tuple(str(i) for i in z_fog_2[1:])),
    location=CsvDataLocation(file=fog.file_path, position=1),
)

el22 = Element(
    timestamp=z_stereo_left_2[0],
    measurement=Measurement(
        sensor=StereoCamera(stereo.name, params),
        values=(
            Image.fromarray(z_stereo_left_2[1]),
            Image.fromarray(z_stereo_right_2[1]),
        ),
    ),
    location=StereoImgDataLocation(
        files=(
            (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_2[0])).with_suffix(
                DatasetStructure.image_file_extension
            ),
            (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_2[0])).with_suffix(
                DatasetStructure.image_file_extension
            ),
        )
    ),
)

el23 = Element(
    timestamp=z_imu_3[0],
    measurement=Measurement(sensor=Encoder(imu.name, params), values=tuple(str(i) for i in z_imu_3[1:])),
    location=CsvDataLocation(file=imu.file_path, position=2),
)

el24 = Element(
    timestamp=z_stereo_left_3[0],
    measurement=Measurement(
        sensor=StereoCamera(stereo.name, params),
        values=(
            Image.fromarray(z_stereo_left_3[1]),
            Image.fromarray(z_stereo_right_3[1]),
        ),
    ),
    location=StereoImgDataLocation(
        files=(
            (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_3[0])).with_suffix(
                DatasetStructure.image_file_extension
            ),
            (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_3[0])).with_suffix(
                DatasetStructure.image_file_extension
            ),
        )
    ),
)

el25 = Element(
    timestamp=z_sick_middle_3[0],
    measurement=Measurement(sensor=Lidar2D(sick_middle.name, params), values=z_sick_middle_3[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_middle_dir / str(z_sick_middle_3[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)


imu_requests: set[PeriodicData] = {
    PeriodicData(
        sensor=el3.measurement.sensor,
        period=TimeRange(start=el3.timestamp, stop=el3.timestamp),
    ),
    PeriodicData(
        sensor=el10.measurement.sensor,
        period=TimeRange(start=el10.timestamp, stop=el10.timestamp),
    ),
    PeriodicData(
        sensor=el23.measurement.sensor,
        period=TimeRange(start=el23.timestamp, stop=el23.timestamp),
    ),
    PeriodicData(
        sensor=el3.measurement.sensor,
        period=TimeRange(start=el3.timestamp, stop=el23.timestamp),
    ),
    PeriodicData(
        sensor=el3.measurement.sensor,
        period=TimeRange(start=el3.timestamp, stop=el10.timestamp),
    ),
    PeriodicData(
        sensor=el10.measurement.sensor,
        period=TimeRange(start=el10.timestamp, stop=el23.timestamp),
    ),
}

imu_batch = DataBatch()
imu_batch.add(el3)
imu_batch.add(el10)
imu_batch.add(el23)


lidar2D_requests: set[PeriodicData] = {
    PeriodicData(
        sensor=el5.measurement.sensor,
        period=TimeRange(start=el5.timestamp, stop=el5.timestamp),
    ),
    PeriodicData(
        sensor=el14.measurement.sensor,
        period=TimeRange(start=el14.timestamp, stop=el14.timestamp),
    ),
    PeriodicData(
        sensor=el25.measurement.sensor,
        period=TimeRange(start=el25.timestamp, stop=el25.timestamp),
    ),
    PeriodicData(
        sensor=el5.measurement.sensor,
        period=TimeRange(start=el5.timestamp, stop=el25.timestamp),
    ),
    PeriodicData(
        sensor=el5.measurement.sensor,
        period=TimeRange(start=el5.timestamp, stop=el14.timestamp),
    ),
    PeriodicData(
        sensor=el14.measurement.sensor,
        period=TimeRange(start=el14.timestamp, stop=el25.timestamp),
    ),
}

lidar2D_batch = DataBatch()
lidar2D_batch.add(el5)
lidar2D_batch.add(el14)
lidar2D_batch.add(el25)


stereo_requests: set[PeriodicData] = {
    PeriodicData(
        sensor=el19.measurement.sensor,
        period=TimeRange(start=el19.timestamp, stop=el19.timestamp),
    ),
    PeriodicData(
        sensor=el22.measurement.sensor,
        period=TimeRange(start=el22.timestamp, stop=el22.timestamp),
    ),
    PeriodicData(
        sensor=el24.measurement.sensor,
        period=TimeRange(start=el24.timestamp, stop=el24.timestamp),
    ),
    PeriodicData(
        sensor=el19.measurement.sensor,
        period=TimeRange(start=el19.timestamp, stop=el24.timestamp),
    ),
    PeriodicData(
        sensor=el19.measurement.sensor,
        period=TimeRange(start=el19.timestamp, stop=el22.timestamp),
    ),
    PeriodicData(
        sensor=el22.measurement.sensor,
        period=TimeRange(start=el22.timestamp, stop=el24.timestamp),
    ),
}

stereo_batch = DataBatch()
stereo_batch.add(el19)
stereo_batch.add(el22)
stereo_batch.add(el24)

common_batch = DataBatch()
common_batch.add(el3)
common_batch.add(el10)
common_batch.add(el23)
common_batch.add(el5)
common_batch.add(el14)
common_batch.add(el25)
common_batch.add(el19)
common_batch.add(el22)
common_batch.add(el24)

common_requests = {*imu_requests, *lidar2D_requests, *stereo_requests}

imu_scenario: tuple[set[PeriodicData], DataBatch] = (imu_requests, imu_batch)
lidar2D_scenario: tuple[set[PeriodicData], DataBatch] = (
    lidar2D_requests,
    lidar2D_batch,
)
stereo_scenario: tuple[set[PeriodicData], DataBatch] = (stereo_requests, stereo_batch)
common_scenario: tuple[set[PeriodicData], DataBatch] = (common_requests, common_batch)

kaist_dataset_requests_scenarios: list[tuple[set[PeriodicData], DataBatch]] = [
    imu_scenario,
    lidar2D_scenario,
    stereo_scenario,
    common_scenario,
]


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
elements_batch = DataBatch()
for el in elements:
    elements_batch.add(el)

kaist_dataset_deque_scenario: tuple[list[Element], DataBatch] = (
    elements,
    elements_batch,
)


b1 = DataBatch()
b2 = DataBatch()
b3 = DataBatch()
b1.add(el1)
b2.add(el25)

for el in itertools.islice(elements, el9.timestamp, el20.timestamp):
    b3.add(el)

scenarios: list[tuple[TimeRange, DataBatch]] = [
    (TimeRange(el1.timestamp, el1.timestamp), b1),
    (TimeRange(el25.timestamp, el25.timestamp), b2),
    (TimeRange(el10.timestamp, el20.timestamp), b3),
]

b4 = DataBatch()
for el in [el3, el10, el23]:
    b4.add(el)

requests: set[PeriodicData] = {
    PeriodicData(
        sensor=el1.measurement.sensor,
        period=TimeRange(start=el1.timestamp, stop=el1.timestamp),
    ),
    PeriodicData(
        sensor=el25.measurement.sensor,
        period=TimeRange(start=el25.timestamp, stop=el25.timestamp),
    ),
    PeriodicData(
        sensor=el3.measurement.sensor,
        period=TimeRange(start=el3.timestamp, stop=el23.timestamp),
    ),
}

b5 = DataBatch()
for el in [el1, el3, el10, el23, el25]:
    b5.add(el)

periodic_request_scenarios: list[tuple[TimeRange, DataBatch, set[PeriodicData]]] = [
    (
        TimeRange(el1.timestamp, el1.timestamp),
        b1,
        {
            PeriodicData(
                sensor=el1.measurement.sensor,
                period=TimeRange(start=el1.timestamp, stop=el1.timestamp),
            )
        },
    ),
    (
        TimeRange(el25.timestamp, el25.timestamp),
        b2,
        {
            PeriodicData(
                sensor=el25.measurement.sensor,
                period=TimeRange(start=el25.timestamp, stop=el25.timestamp),
            )
        },
    ),
    (
        TimeRange(el3.timestamp, el23.timestamp),
        b4,
        {
            PeriodicData(
                sensor=el3.measurement.sensor,
                period=TimeRange(start=el3.timestamp, stop=el23.timestamp),
            )
        },
    ),
    (TimeRange(el1.timestamp, el25.timestamp), b5, requests),
]

incorrect_scenario: list[tuple[TimeRange, DataBatch, set[PeriodicData]]] = [
    (
        TimeRange(el10.timestamp, el20.timestamp),
        b3,
        {
            PeriodicData(
                sensor=el3.measurement.sensor,
                period=TimeRange(start=el3.timestamp, stop=el23.timestamp),
            )
        },
    ),
]
