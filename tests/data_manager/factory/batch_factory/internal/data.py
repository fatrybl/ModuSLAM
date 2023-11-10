from dataclasses import dataclass
from pathlib import Path

from numpy import ones, uint8
from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module
from PIL import Image

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.element_factory import (
    Element, Measurement)
from slam.data_manager.factory.readers.kaist.data_classes import (
    BinaryDataLocation, CsvDataLocation, StereoImgDataLocation)
from slam.setup_manager.sensor_factory.sensors import (
    Imu, Fog, Encoder, Altimeter, Gps,
    VrsGps, Lidar2D, Lidar3D, StereoCamera)
from slam.utils.auxiliary_dataclasses import PeriodicData, TimeRange
from tests.data_manager.auxiliary_utils.kaist_data_factory import SensorNamePath

from configs.paths.kaist_dataset import KaistDatasetPathConfig
from configs.sensors.base_sensor_parameters import ParameterConfig
from configs.paths.kaist_dataset import KaistDatasetPathConfig

from tests.data_manager.factory.readers.kaist.conftest import SENSOR_CONFIG_NAME
from tests.data_manager.factory.batch_factory.internal.config import DATASET_DIR

cs = ConfigStore.instance()
cs.store(name=SENSOR_CONFIG_NAME, node=ParameterConfig)
with initialize_config_module(config_module="tests.data_manager.factory.batch_factory.api.conf"):
    params = compose(config_name=SENSOR_CONFIG_NAME)


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
    calibration_data_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.calibration_data_dir
    sensor_data_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.sensor_data_dir
    image_data_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.image_data_dir
    data_stamp: Path = dataset_directory / \
        KaistDatasetPathConfig.data_stamp
    lidar_2D_back_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.lidar_2D_back_dir
    lidar_2D_middle_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.lidar_2D_middle_dir
    lidar_3D_left_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.lidar_3D_left_dir
    lidar_3D_right_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.lidar_3D_right_dir
    stereo_left_data_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.image_data_dir / \
        KaistDatasetPathConfig.stereo_left_data_dir
    stereo_right_data_dir: Path = dataset_directory / \
        KaistDatasetPathConfig.image_data_dir / \
        KaistDatasetPathConfig.stereo_right_data_dir

    imu_data_file: Path = dataset_directory / \
        KaistDatasetPathConfig.imu_data_file
    fog_data_file: Path = dataset_directory / \
        KaistDatasetPathConfig.fog_data_file
    encoder_data_file: Path = dataset_directory / \
        KaistDatasetPathConfig.encoder_data_file
    altimeter_data_file: Path = dataset_directory / \
        KaistDatasetPathConfig.altimeter_data_file
    gps_data_file: Path = dataset_directory / \
        KaistDatasetPathConfig.gps_data_file
    vrs_gps_data_file: Path = dataset_directory / \
        KaistDatasetPathConfig.vrs_gps_data_file
    lidar_2D_back_stamp_file: Path = dataset_directory / \
        KaistDatasetPathConfig.lidar_2D_back_stamp_file
    lidar_2D_middle_stamp_file: Path = dataset_directory / \
        KaistDatasetPathConfig.lidar_2D_middle_stamp_file
    lidar_3D_left_stamp_file: Path = dataset_directory / \
        KaistDatasetPathConfig.lidar_3D_left_stamp_file
    lidar_3D_right_stamp_file: Path = dataset_directory / \
        KaistDatasetPathConfig.lidar_3D_right_stamp_file
    stereo_stamp_file: Path = dataset_directory / \
        KaistDatasetPathConfig.stereo_stamp_file

    binary_file_extension: str = '.bin'
    image_file_extension: str = '.png'


# sensor stamp files
imu = SensorNamePath(
    'imu', DatasetStructure.imu_data_file)
fog = SensorNamePath(
    'fog', DatasetStructure.fog_data_file)
encoder = SensorNamePath(
    'encoder', DatasetStructure.encoder_data_file)
altimeter = SensorNamePath(
    'altimeter', DatasetStructure.altimeter_data_file)
gps = SensorNamePath(
    'gps', DatasetStructure.gps_data_file)
vrs_gps = SensorNamePath(
    'vrs', DatasetStructure.vrs_gps_data_file)
sick_back = SensorNamePath(
    'sick_back', DatasetStructure.lidar_2D_back_stamp_file)
sick_middle = SensorNamePath(
    'sick_middle', DatasetStructure.lidar_2D_middle_stamp_file)
velodyne_left = SensorNamePath(
    'velodyne_left', DatasetStructure.lidar_3D_left_stamp_file)
velodyne_right = SensorNamePath(
    'velodyne_right', DatasetStructure.lidar_3D_right_stamp_file)
stereo = SensorNamePath(
    'stereo', DatasetStructure.stereo_stamp_file)

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
    [9, velodyne_left.name],
    [10, velodyne_right.name],
    [11, stereo.name],
    [12, encoder.name],
    [13, encoder.name],
    [14, encoder.name],
    [15, sick_back.name],
    [16, sick_back.name],
    [17, sick_back.name],
    [18, stereo.name],
    [19, stereo.name],
    [20, stereo.name],
]

# raw measurements
z_encoder_1 = (1, 1.0, 1.0, 1.0)
z_encoder_2 = (12, 1.0, 1.0, 1.0)
z_encoder_3 = (13, 1.0, 1.0, 1.0)
z_encoder_4 = (14, 1.0, 1.0, 1.0)
z_sick_back_1 = (2, 1.0, 1.0, 1.0)
z_sick_back_2 = (15, 1.0, 1.0, 1.0)
z_sick_back_3 = (16, 1.0, 1.0, 1.0)
z_sick_back_4 = (17, 1.0, 1.0, 1.0)
z_imu_1 = (3, 1.0, 1.0, 1.0)
z_fog_1 = (4, 1.0, 1.0, 1.0)
z_sick_middle_1 = (5, 1.0, 1.0, 1.0)
z_gps_1 = (6, 1.0, 1.0, 1.0)
z_vrs_gps_1 = (7, 1.0, 1.0, 1.0)
z_altimeter_1 = (8, 1.0, 1.0, 1.0)
z_velodyne_left_1 = (9, 1.0, 1.0, 1.0)
z_velodyne_right_1 = (10, 1.0, 1.0, 1.0)
z_stereo_left_1 = (11, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_right_1 = (11, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_left_2 = (18, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_right_2 = (18, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_left_3 = (19, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_right_3 = (19, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_left_4 = (20, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_right_4 = (20, ones(shape=(2, 2, 3)).astype(uint8))


binary_data = [(z_sick_back_1[1:],
                (DatasetStructure.lidar_2D_back_dir / str(z_sick_back_1[0])).with_suffix(DatasetStructure.binary_file_extension)),
               (z_sick_back_2[1:],
                (DatasetStructure.lidar_2D_back_dir / str(z_sick_back_2[0])).with_suffix(DatasetStructure.binary_file_extension)),
               (z_sick_back_3[1:],
                (DatasetStructure.lidar_2D_back_dir / str(z_sick_back_3[0])).with_suffix(DatasetStructure.binary_file_extension)),
               (z_sick_back_4[1:],
                (DatasetStructure.lidar_2D_back_dir / str(z_sick_back_4[0])).with_suffix(DatasetStructure.binary_file_extension)),
               (z_sick_middle_1[1:],
                (DatasetStructure.lidar_2D_middle_dir / str(z_sick_middle_1[0])).with_suffix(DatasetStructure.binary_file_extension)),
               (z_velodyne_left_1[1:],
                (DatasetStructure.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(DatasetStructure.binary_file_extension)),
               (z_velodyne_right_1[1:],
                (DatasetStructure.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(DatasetStructure.binary_file_extension))]

image_data = [(z_stereo_left_1,
               (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_1[0])).with_suffix(DatasetStructure.image_file_extension)),
              (z_stereo_right_1,
               (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_1[0])).with_suffix(DatasetStructure.image_file_extension)),
              (z_stereo_left_2,
               (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_2[0])).with_suffix(DatasetStructure.image_file_extension)),
              (z_stereo_right_2,
               (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_2[0])).with_suffix(DatasetStructure.image_file_extension)),
              (z_stereo_left_3,
               (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_3[0])).with_suffix(DatasetStructure.image_file_extension)),
              (z_stereo_right_3,
               (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_3[0])).with_suffix(DatasetStructure.image_file_extension)),
              (z_stereo_left_4,
               (DatasetStructure.stereo_left_data_dir / str(z_stereo_left_4[0])).with_suffix(DatasetStructure.image_file_extension)),
              (z_stereo_right_4,
               (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_4[0])).with_suffix(DatasetStructure.image_file_extension)),]

csv_data = [(z_imu_1, imu.file_path),
            (z_fog_1, fog.file_path),
            (z_gps_1, gps.file_path),
            (z_vrs_gps_1, vrs_gps.file_path),
            (z_altimeter_1, altimeter.file_path),
            (z_encoder_1, encoder.file_path),
            (z_encoder_2, encoder.file_path),
            (z_encoder_3, encoder.file_path),
            (z_encoder_4, encoder.file_path),]

stamp_files = [([z_sick_back_1[0]], sick_back.file_path),
               ([z_sick_back_2[0]], sick_back.file_path),
               ([z_sick_back_3[0]], sick_back.file_path),
               ([z_sick_back_4[0]], sick_back.file_path),
               ([z_sick_middle_1[0]], sick_middle.file_path),
               ([z_velodyne_left_1[0]], velodyne_left.file_path),
               ([z_velodyne_right_1[0]], velodyne_right.file_path),
               ([z_stereo_left_1[0]], stereo.file_path),
               ([z_stereo_left_2[0]], stereo.file_path),
               ([z_stereo_left_3[0]], stereo.file_path),
               ([z_stereo_left_4[0]], stereo.file_path),]

el1 = Element(
    timestamp=z_encoder_1[0],
    measurement=Measurement(
        sensor=Encoder(encoder.name, params),
        values=tuple(str(i) for i in z_encoder_1[1:])),
    location=CsvDataLocation(
        file=encoder.file_path,
        position=0))

el2 = Element(
    timestamp=z_sick_back_1[0],
    measurement=Measurement(
        sensor=Lidar2D(sick_back.name, params),
        values=z_sick_back_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_back_dir /
              str(z_sick_back_1[0])).with_suffix(DatasetStructure.binary_file_extension)))

el3 = Element(
    timestamp=z_imu_1[0],
    measurement=Measurement(
        sensor=Imu(imu.name, params),
        values=tuple(str(i) for i in z_imu_1[1:])),
    location=CsvDataLocation(
        file=imu.file_path,
        position=0))

el4 = Element(
    timestamp=z_fog_1[0],
    measurement=Measurement(
        sensor=Fog(fog.name, params),
        values=tuple(str(i) for i in z_fog_1[1:])),
    location=CsvDataLocation(
        file=fog.file_path,
        position=0))

el5 = Element(
    timestamp=z_sick_middle_1[0],
    measurement=Measurement(
        sensor=Lidar2D(sick_middle.name, params),
        values=z_sick_middle_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_middle_dir /
              str(z_sick_middle_1[0])).with_suffix(DatasetStructure.binary_file_extension)))

el6 = Element(
    timestamp=z_gps_1[0],
    measurement=Measurement(
        sensor=Gps(gps.name, params),
        values=tuple(str(i) for i in z_gps_1[1:])),
    location=CsvDataLocation(
        file=gps.file_path,
        position=0))

el7 = Element(
    timestamp=z_vrs_gps_1[0],
    measurement=Measurement(
        sensor=VrsGps(vrs_gps.name, params),
        values=tuple(str(i) for i in z_vrs_gps_1[1:])),
    location=CsvDataLocation(
        file=vrs_gps.file_path,
        position=0))

el8 = Element(
    timestamp=z_altimeter_1[0],
    measurement=Measurement(
        sensor=Altimeter(altimeter.name, params),
        values=tuple(str(i) for i in z_altimeter_1[1:])),
    location=CsvDataLocation(
        file=altimeter.file_path,
        position=0))

el9 = Element(
    timestamp=z_velodyne_left_1[0],
    measurement=Measurement(
        sensor=Lidar3D(velodyne_left.name, params),
        values=z_velodyne_left_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_3D_left_dir /
              str(z_velodyne_left_1[0])).with_suffix(DatasetStructure.binary_file_extension)))

el10 = Element(
    timestamp=z_velodyne_right_1[0],
    measurement=Measurement(
        sensor=Lidar3D(velodyne_right.name, params),
        values=z_velodyne_right_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_3D_right_dir /
              str(z_velodyne_right_1[0])).with_suffix(DatasetStructure.binary_file_extension)))

el11 = Element(
    timestamp=z_stereo_left_1[0],
    measurement=Measurement(
        sensor=StereoCamera(stereo.name, params),
        values=(Image.fromarray(z_stereo_left_1[1]),
                Image.fromarray(z_stereo_right_1[1]))),
    location=StereoImgDataLocation(
        files=(
            (DatasetStructure.stereo_left_data_dir /
             str(z_stereo_left_1[0])).with_suffix(DatasetStructure.image_file_extension),
            (DatasetStructure.stereo_right_data_dir /
             str(z_stereo_right_1[0])).with_suffix(DatasetStructure.image_file_extension))))

el12 = Element(
    timestamp=z_encoder_2[0],
    measurement=Measurement(
        sensor=Encoder(encoder.name, params),
        values=tuple(str(i) for i in z_encoder_2[1:])),
    location=CsvDataLocation(
        file=encoder.file_path,
        position=1))

el13 = Element(
    timestamp=z_encoder_3[0],
    measurement=Measurement(
        sensor=Encoder(encoder.name, params),
        values=tuple(str(i) for i in z_encoder_3[1:])),
    location=CsvDataLocation(
        file=encoder.file_path,
        position=2))

el14 = Element(
    timestamp=z_encoder_4[0],
    measurement=Measurement(
        sensor=Encoder(encoder.name, params),
        values=tuple(str(i) for i in z_encoder_4[1:])),
    location=CsvDataLocation(
        file=encoder.file_path,
        position=3))

el15 = Element(
    timestamp=z_sick_back_2[0],
    measurement=Measurement(
        sensor=Lidar2D(sick_back.name, params),
        values=z_sick_back_2[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_back_dir /
              str(z_sick_back_2[0])).with_suffix(DatasetStructure.binary_file_extension)))


el16 = Element(
    timestamp=z_sick_back_3[0],
    measurement=Measurement(
        sensor=Lidar2D(sick_back.name, params),
        values=z_sick_back_3[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_back_dir /
              str(z_sick_back_3[0])).with_suffix(DatasetStructure.binary_file_extension)))


el17 = Element(
    timestamp=z_sick_back_4[0],
    measurement=Measurement(
        sensor=Lidar2D(sick_back.name, params),
        values=z_sick_back_4[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_2D_back_dir /
              str(z_sick_back_4[0])).with_suffix(DatasetStructure.binary_file_extension)))

el18 = Element(
    timestamp=z_stereo_left_2[0],
    measurement=Measurement(
        sensor=StereoCamera(stereo.name, params),
        values=(Image.fromarray(z_stereo_left_2[1]),
                Image.fromarray(z_stereo_right_2[1]))),
    location=StereoImgDataLocation(
        files=(
            (DatasetStructure.stereo_left_data_dir /
             str(z_stereo_left_2[0])).with_suffix(DatasetStructure.image_file_extension),
            (DatasetStructure.stereo_right_data_dir /
             str(z_stereo_right_2[0])).with_suffix(DatasetStructure.image_file_extension))))

el19 = Element(
    timestamp=z_stereo_left_3[0],
    measurement=Measurement(
        sensor=StereoCamera(stereo.name, params),
        values=(Image.fromarray(z_stereo_left_3[1]),
                Image.fromarray(z_stereo_right_3[1]))),
    location=StereoImgDataLocation(
        files=(
            (DatasetStructure.stereo_left_data_dir /
             str(z_stereo_left_3[0])).with_suffix(DatasetStructure.image_file_extension),
            (DatasetStructure.stereo_right_data_dir /
             str(z_stereo_right_3[0])).with_suffix(DatasetStructure.image_file_extension))))

el20 = Element(
    timestamp=z_stereo_left_4[0],
    measurement=Measurement(
        sensor=StereoCamera(stereo.name, params),
        values=(Image.fromarray(z_stereo_left_4[1]),
                Image.fromarray(z_stereo_right_4[1]))),
    location=StereoImgDataLocation(
        files=(
            (DatasetStructure.stereo_left_data_dir /
             str(z_stereo_left_4[0])).with_suffix(DatasetStructure.image_file_extension),
            (DatasetStructure.stereo_right_data_dir /
             str(z_stereo_right_4[0])).with_suffix(DatasetStructure.image_file_extension))))


encoder_requests: list[PeriodicData] = [
    PeriodicData(sensor=el1.measurement.sensor,
                 period=TimeRange(start=el1.timestamp,
                                  stop=el1.timestamp)),
    PeriodicData(sensor=el14.measurement.sensor,
                 period=TimeRange(start=el14.timestamp,
                                  stop=el14.timestamp)),
    PeriodicData(sensor=el12.measurement.sensor,
                 period=TimeRange(start=el12.timestamp,
                                  stop=el12.timestamp)),
    PeriodicData(sensor=el1.measurement.sensor,
                 period=TimeRange(start=el1.timestamp,
                                  stop=el14.timestamp)),
    PeriodicData(sensor=el12.measurement.sensor,
                 period=TimeRange(start=el12.timestamp,
                                  stop=el13.timestamp)),
    PeriodicData(sensor=el1.measurement.sensor,
                 period=TimeRange(start=el1.timestamp,
                                  stop=el12.timestamp)),
    PeriodicData(sensor=el13.measurement.sensor,
                 period=TimeRange(start=el13.timestamp,
                                  stop=el14.timestamp)),
    PeriodicData(sensor=el1.measurement.sensor,
                 period=TimeRange(start=el1.timestamp,
                                  stop=el13.timestamp)),
    PeriodicData(sensor=el12.measurement.sensor,
                 period=TimeRange(start=el12.timestamp,
                                  stop=el14.timestamp)), ]

batch1, batch2, batch3, batch4, batch5, batch6, batch7, batch8, batch9 = DataBatch(), DataBatch(
),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch()

batch1.add(el1)
batch2.add(el14)
batch3.add(el12)
batch4.add(el1)
batch4.add(el12)
batch4.add(el13)
batch4.add(el14)
batch5.add(el12)
batch5.add(el13)
batch6.add(el1)
batch6.add(el12)
batch7.add(el13)
batch7.add(el14)
batch8.add(el1)
batch8.add(el12)
batch8.add(el13)
batch9.add(el12)
batch9.add(el13)
batch9.add(el14)


encoder_batches: list[DataBatch] = [batch1, batch2, batch3, batch4, batch5,
                                    batch6, batch7, batch8, batch9]

encoder_scenarios: list[tuple[PeriodicData, DataBatch]] = list(
    zip(encoder_requests, encoder_batches))


lidar2D_requests: list[PeriodicData] = [
    PeriodicData(sensor=el2.measurement.sensor,
                 period=TimeRange(start=el2.timestamp,
                                  stop=el2.timestamp)),
    PeriodicData(sensor=el17.measurement.sensor,
                 period=TimeRange(start=el17.timestamp,
                                  stop=el17.timestamp)),
    PeriodicData(sensor=el15.measurement.sensor,
                 period=TimeRange(start=el15.timestamp,
                                  stop=el15.timestamp)),
    PeriodicData(sensor=el2.measurement.sensor,
                 period=TimeRange(start=el2.timestamp,
                                  stop=el17.timestamp)),
    PeriodicData(sensor=el15.measurement.sensor,
                 period=TimeRange(start=el15.timestamp,
                                  stop=el16.timestamp)),
    PeriodicData(sensor=el2.measurement.sensor,
                 period=TimeRange(start=el2.timestamp,
                                  stop=el15.timestamp)),
    PeriodicData(sensor=el16.measurement.sensor,
                 period=TimeRange(start=el16.timestamp,
                                  stop=el17.timestamp)),
    PeriodicData(sensor=el2.measurement.sensor,
                 period=TimeRange(start=el2.timestamp,
                                  stop=el16.timestamp)),
    PeriodicData(sensor=el15.measurement.sensor,
                 period=TimeRange(start=el15.timestamp,
                                  stop=el17.timestamp)), ]

batch1, batch2, batch3, batch4, batch5, batch6, batch7, batch8, batch9 = DataBatch(), DataBatch(
),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch()

batch1.add(el2)
batch2.add(el17)
batch3.add(el15)
batch4.add(el2)
batch4.add(el15)
batch4.add(el16)
batch4.add(el17)
batch5.add(el15)
batch5.add(el16)
batch6.add(el2)
batch6.add(el15)
batch7.add(el16)
batch7.add(el17)
batch8.add(el2)
batch8.add(el15)
batch8.add(el16)
batch9.add(el15)
batch9.add(el16)
batch9.add(el17)

lidar2D_batches: list[DataBatch] = [batch1, batch2, batch3, batch4, batch5,
                                    batch6, batch7, batch8, batch9]

lidar2D_scenarios: list[tuple[PeriodicData, DataBatch]] = list(
    zip(lidar2D_requests, lidar2D_batches))


stereo_requests: list[PeriodicData] = [
    PeriodicData(sensor=el11.measurement.sensor,
                 period=TimeRange(start=el11.timestamp,
                                  stop=el11.timestamp)),
    PeriodicData(sensor=el20.measurement.sensor,
                 period=TimeRange(start=el20.timestamp,
                                  stop=el20.timestamp)),
    PeriodicData(sensor=el19.measurement.sensor,
                 period=TimeRange(start=el19.timestamp,
                                  stop=el19.timestamp)),
    PeriodicData(sensor=el11.measurement.sensor,
                 period=TimeRange(start=el11.timestamp,
                                  stop=el20.timestamp)),
    PeriodicData(sensor=el18.measurement.sensor,
                 period=TimeRange(start=el18.timestamp,
                                  stop=el19.timestamp)),
    PeriodicData(sensor=el11.measurement.sensor,
                 period=TimeRange(start=el11.timestamp,
                                  stop=el18.timestamp)),
    PeriodicData(sensor=el19.measurement.sensor,
                 period=TimeRange(start=el19.timestamp,
                                  stop=el20.timestamp)),
    PeriodicData(sensor=el11.measurement.sensor,
                 period=TimeRange(start=el11.timestamp,
                                  stop=el19.timestamp)),
    PeriodicData(sensor=el18.measurement.sensor,
                 period=TimeRange(start=el18.timestamp,
                                  stop=el20.timestamp)), ]

batch1, batch2, batch3, batch4, batch5, batch6, batch7, batch8, batch9 = DataBatch(), DataBatch(
),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch(),  DataBatch()

batch1.add(el11)
batch2.add(el20)
batch3.add(el19)
batch4.add(el11)
batch4.add(el18)
batch4.add(el19)
batch4.add(el20)
batch5.add(el18)
batch5.add(el19)
batch6.add(el11)
batch6.add(el18)
batch7.add(el19)
batch7.add(el20)
batch8.add(el11)
batch8.add(el18)
batch8.add(el19)
batch9.add(el18)
batch9.add(el19)
batch9.add(el20)

stereo_batches: list[DataBatch] = [batch1, batch2, batch3, batch4, batch5,
                                   batch6, batch7, batch8, batch9]

stereo_scenarios: list[tuple[PeriodicData, DataBatch]] = list(
    zip(stereo_requests, stereo_batches))
