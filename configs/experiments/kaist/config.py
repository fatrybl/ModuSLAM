from dataclasses import dataclass, field
from pathlib import Path

from configs.paths.kaist_dataset import KaistDatasetPathConfig as KaistPaths
from configs.sensors.altimeter import AltimeterParameter
from configs.sensors.encoder import EncoderParameter
from configs.sensors.fog import FogParameter
from configs.sensors.gps import GpsParameter
from configs.sensors.imu import ImuParameter
from configs.sensors.sick_back import SickBackParameter
from configs.sensors.sick_middle import SickMiddleParameter
from configs.sensors.stereo import StereoParameter
from configs.sensors.velodyne_left import VelodyneLeftParameter
from configs.sensors.velodyne_right import VelodyneRightParameter
from configs.sensors.vrs_gps import VrsGpsParameter
from configs.system.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
    RegimeConfig,
)
from configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from configs.system.data_manager.batch_factory.datasets.kaist import (
    KaistConfig,
    PairConfig,
)
from configs.system.data_manager.batch_factory.memory import MemoryAnalyzerConfig
from configs.system.data_manager.batch_factory.regime import (
    StreamConfig,
    TimeLimitConfig,
)
from configs.system.data_manager.data_manager import DataManagerConfig
from configs.system.frontend_manager.edge_factories.imu_odometry import (
    ImuOdometryFactoryConfig,
)
from configs.system.frontend_manager.edge_factories.smart_landmark import (
    SmartStereoFeaturesFactoryConfig,
)
from configs.system.frontend_manager.element_distributor.element_distributor import (
    ElementDistributorConfig,
)
from configs.system.frontend_manager.frontend_manager import FrontendManagerConfig
from configs.system.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)
from configs.system.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)
from configs.system.frontend_manager.handlers.base_handler import HandlerConfig
from configs.system.setup_manager.handler_factory import HandlerFactoryConfig
from configs.system.setup_manager.sensor_factory import (
    SensorConfig,
    SensorFactoryConfig,
)
from configs.system.setup_manager.setup_manager import SetupManagerConfig
from slam.frontend_manager.graph.edges_factories.imu_odometry_factory import (
    ImuOdometryFactory,
)
from slam.frontend_manager.graph.edges_factories.smart_stereo_landmark_factory import (
    SmartStereoFeaturesFactory,
)
from slam.frontend_manager.graph_builder.builders.lidar_pointcloud_builder import (
    PointCloudBuilder,
)
from slam.frontend_manager.handlers.imu_preintegration import ImuPreintegration
from slam.frontend_manager.handlers.stereo_features import SmartStereoFeatures
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

imu = SensorConfig("imu", Imu.__name__, ImuParameter())
fog = SensorConfig("fog", Fog.__name__, FogParameter())
encoder = SensorConfig("encoder", Encoder.__name__, EncoderParameter())
altimeter = SensorConfig("altimeter", Altimeter.__name__, AltimeterParameter())
gps = SensorConfig("gps", Gps.__name__, GpsParameter())
vrs_gps = SensorConfig("vrs", VrsGps.__name__, VrsGpsParameter())
stereo = SensorConfig("stereo", StereoCamera.__name__, StereoParameter())
lidar_3D_right = SensorConfig("velodyne_right", Lidar3D.__name__, VelodyneLeftParameter())
lidar_3D_left = SensorConfig("velodyne_left", Lidar3D.__name__, VelodyneRightParameter())
lidar_2D_back = SensorConfig("sick_back", Lidar2D.__name__, SickBackParameter())
lidar_2D_middle = SensorConfig("sick_middle", Lidar2D.__name__, SickMiddleParameter())


all_sensors: list[SensorConfig] = [
    imu,
    fog,
    encoder,
    stereo,
    altimeter,
    gps,
    vrs_gps,
    lidar_3D_right,
    lidar_3D_left,
    lidar_2D_middle,
    lidar_2D_back,
]

used_sensors: list[SensorConfig] = [
    imu,
    fog,
    encoder,
    stereo,
    altimeter,
    gps,
    vrs_gps,
    lidar_3D_right,
    lidar_3D_left,
    lidar_2D_middle,
    lidar_2D_back,
]


dataset_directory: Path = Path("/home/oem/Downloads/urban19-highway/")


iterable_data_files: list[PairConfig] = [
    PairConfig(imu.name, dataset_directory / KaistPaths.imu_data_file),
    PairConfig(fog.name, dataset_directory / KaistPaths.fog_data_file),
    PairConfig(encoder.name, dataset_directory / KaistPaths.encoder_data_file),
    PairConfig(altimeter.name, dataset_directory / KaistPaths.altimeter_data_file),
    PairConfig(gps.name, dataset_directory / KaistPaths.gps_data_file),
    PairConfig(vrs_gps.name, dataset_directory / KaistPaths.vrs_gps_data_file),
    PairConfig(stereo.name, dataset_directory / KaistPaths.stereo_stamp_file),
    PairConfig(lidar_2D_back.name, dataset_directory / KaistPaths.lidar_2D_back_stamp_file),
    PairConfig(
        lidar_2D_middle.name,
        dataset_directory / KaistPaths.lidar_2D_middle_stamp_file,
    ),
    PairConfig(lidar_3D_left.name, dataset_directory / KaistPaths.lidar_3D_left_stamp_file),
    PairConfig(
        lidar_3D_right.name,
        dataset_directory / KaistPaths.lidar_3D_right_stamp_file,
    ),
]


data_dirs: list[PairConfig] = [
    PairConfig(stereo.name, dataset_directory / KaistPaths.image_data_dir),
    PairConfig(lidar_2D_back.name, dataset_directory / KaistPaths.lidar_2D_back_dir),
    PairConfig(lidar_2D_middle.name, dataset_directory / KaistPaths.lidar_2D_middle_dir),
    PairConfig(lidar_3D_left.name, dataset_directory / KaistPaths.lidar_3D_left_dir),
    PairConfig(lidar_3D_right.name, dataset_directory / KaistPaths.lidar_3D_right_dir),
]


imu_handler = HandlerConfig(
    name=imu.name,
    type_name=ImuPreintegration.__name__,
    module_name=".imu_preintegration",
)
stereo_handler = HandlerConfig(
    name=stereo.name,
    type_name=SmartStereoFeatures.__name__,
    module_name=".stereo_features",
)

handlers: list[HandlerConfig] = [imu_handler, stereo_handler]

imu_odometry_factory = ImuOdometryFactoryConfig("imu_odometry_factory", ImuOdometryFactory.__name__)
smart_stereo_features_factory = SmartStereoFeaturesFactoryConfig(
    "smart_stereo_features_factory", SmartStereoFeaturesFactory.__name__
)


class MeasurementsFlowTable:
    """
    Sensor->Handler->EdgeFactory table.
    """

    sensor_handlers_table: dict[str, list[str]] = {
        imu.name: [imu_handler.name],
        stereo.name: [stereo_handler.name],
    }

    handler_edge_factory_table: dict[str, str] = {
        imu_handler.name: imu_odometry_factory.name,
        stereo_handler.name: smart_stereo_features_factory.name,
    }


@dataclass
class KaistDS(KaistConfig):
    reader = "KaistReader"
    directory: Path = dataset_directory
    iterable_data_files: list[PairConfig] = field(default_factory=lambda: iterable_data_files)
    data_dirs: list[PairConfig] = field(default_factory=lambda: data_dirs)


@dataclass
class Memory(MemoryAnalyzerConfig):
    graph_memory: float = 10.0


@dataclass
class TLimit(TimeLimitConfig):
    start: int = 1544578682416523355
    stop: int = 1544578682426144851


@dataclass
class SF(SensorFactoryConfig):
    all_sensors: list[SensorConfig] = field(default_factory=lambda: all_sensors)
    used_sensors: list[SensorConfig] = field(default_factory=lambda: used_sensors)


@dataclass
class HF(HandlerFactoryConfig):
    package_name: str = "slam.frontend_manager.handlers"
    handlers: list[HandlerConfig] = field(default_factory=lambda: handlers)


@dataclass
class SM(SetupManagerConfig):
    sensor_factory: SensorFactoryConfig = field(default_factory=SF)
    handler_factory: HandlerFactoryConfig = field(default_factory=HF)


@dataclass
class BF(BatchFactoryConfig):
    dataset: DatasetConfig = field(default_factory=KaistDS)
    memory: MemoryAnalyzerConfig = field(default_factory=Memory)
    regime: RegimeConfig = field(default_factory=StreamConfig)


@dataclass
class DM(DataManagerConfig):
    batch_factory: BatchFactoryConfig = field(default_factory=BF)


@dataclass
class ED(ElementDistributorConfig):
    sensor_handlers_table: dict[str, list[str]] = field(
        default_factory=lambda: MeasurementsFlowTable.sensor_handlers_table
    )


@dataclass
class GM(GraphMergerConfig):
    handler_edge_factory_table: dict[str, str] = field(
        default_factory=lambda: MeasurementsFlowTable.handler_edge_factory_table
    )


@dataclass
class GB(GraphBuilderConfig):
    class_name: str = PointCloudBuilder.__name__
    element_distributor: ElementDistributorConfig = field(default_factory=ED)
    graph_merger: GraphMergerConfig = field(default_factory=GM)


@dataclass
class FM(FrontendManagerConfig):
    graph_builder: GraphBuilderConfig = field(default_factory=GB)


@dataclass
class Config:
    setup_manager: SetupManagerConfig = field(default_factory=SM)
    data_manager: DataManagerConfig = field(default_factory=DM)
    frontend_manager: FrontendManagerConfig = field(default_factory=FM)
    # backend_manager: BackendManagerConfig = field(default_factory=BackendManagerConfig)
    # map_manager: MapManagerConfig = field(default_factory=MapManagerConfig)
