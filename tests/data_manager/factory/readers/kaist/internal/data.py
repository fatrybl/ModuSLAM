from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from hydra import compose, initialize_config_module
from hydra.core.config_store import ConfigStore
from numpy import ones, uint8

from configs.paths.kaist_dataset import KaistDatasetPathConfig
from configs.sensors.base_sensor_parameters import ParameterConfig
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
from tests.data_manager.auxiliary_utils.kaist_data_factory import (
    SensorElementPair,
    SensorNamePath,
)
from tests.data_manager.factory.readers.kaist.conftest import SENSOR_FACTORY_CONFIG_NAME
from tests.data_manager.factory.readers.kaist.internal.config import DATASET_DIR

cs = ConfigStore.instance()
cs.store(name=SENSOR_FACTORY_CONFIG_NAME, node=ParameterConfig)
with initialize_config_module(config_module="tests.data_manager.factory.batch_factory.api.conf"):
    params = compose(config_name=SENSOR_FACTORY_CONFIG_NAME)


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
    [9, velodyne_left.name],
    [10, velodyne_right.name],
    [11, stereo.name],
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
z_velodyne_left_1 = (9, 1.0, 1.0, 1.0)
z_velodyne_right_1 = (10, 1.0, 1.0, 1.0)
z_stereo_left_1 = (11, ones(shape=(2, 2, 3)).astype(uint8))
z_stereo_right_1 = (11, ones(shape=(2, 2, 3)).astype(uint8))

binary_data = [
    (
        z_sick_back_1[1:],
        (DatasetStructure.lidar_2D_back_dir / str(z_sick_back_1[0])).with_suffix(
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
        z_velodyne_left_1[1:],
        (DatasetStructure.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        ),
    ),
    (
        z_velodyne_right_1[1:],
        (DatasetStructure.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(
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
        z_stereo_right_1,
        (DatasetStructure.stereo_right_data_dir / str(z_stereo_right_1[0])).with_suffix(
            DatasetStructure.image_file_extension
        ),
    ),
]

csv_data = [
    (z_imu_1, imu.file_path),
    (z_fog_1, fog.file_path),
    (z_gps_1, gps.file_path),
    (z_vrs_gps_1, vrs_gps.file_path),
    (z_altimeter_1, altimeter.file_path),
    (z_encoder_1, encoder.file_path),
]

stamp_files = [
    ([z_sick_back_1[0]], sick_back.file_path),
    ([z_sick_middle_1[0]], sick_middle.file_path),
    ([z_velodyne_left_1[0]], velodyne_left.file_path),
    ([z_velodyne_right_1[0]], velodyne_right.file_path),
    ([z_stereo_left_1[0]], stereo.file_path),
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
    timestamp=z_velodyne_left_1[0],
    measurement=Measurement(sensor=Lidar3D(velodyne_left.name, params), values=z_velodyne_left_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_3D_left_dir / str(z_velodyne_left_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el10 = Element(
    timestamp=z_velodyne_right_1[0],
    measurement=Measurement(sensor=Lidar3D(velodyne_right.name, params), values=z_velodyne_right_1[1:]),
    location=BinaryDataLocation(
        file=(DatasetStructure.lidar_3D_right_dir / str(z_velodyne_right_1[0])).with_suffix(
            DatasetStructure.binary_file_extension
        )
    ),
)

el11 = Element(
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

elements: list[Element] = [el1, el2, el3, el4, el5, el6, el7, el8, el9, el10, el11]

sensor_element_pairs = [
    SensorElementPair(Encoder(encoder.name, params), el1),
    SensorElementPair(Lidar2D(sick_back.name, params), el2),
    SensorElementPair(
        Imu(imu.name, params),
        el3,
    ),
    SensorElementPair(
        Fog(fog.name, params),
        el4,
    ),
    SensorElementPair(Lidar2D(sick_middle.name, params), el5),
    SensorElementPair(Gps(gps.name, params), el6),
    SensorElementPair(VrsGps(vrs_gps.name, params), el7),
    SensorElementPair(Altimeter(altimeter.name, params), el8),
    SensorElementPair(Lidar3D(velodyne_left.name, params), el9),
    SensorElementPair(Lidar3D(velodyne_right.name, params), el10),
    SensorElementPair(StereoCamera(stereo.name, params), el11),
]
