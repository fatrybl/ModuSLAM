import pytest

from moduslam.data_manager.factory.batch import DataBatch
from moduslam.data_manager.factory.element import Element
from moduslam.frontend_manager.edge_factories.lidar_odometry import (
    LidarOdometryEdgeFactory,
)
from moduslam.frontend_manager.graph_builder.builders.lidar_map_builder import (
    LidarMapBuilder,
)
from moduslam.frontend_manager.graph_builder.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from moduslam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher
from moduslam.setup_manager.setup_manager import SetupManager
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.system_configs.frontend_manager.element_distributor.element_distributor import (
    ElementDistributorConfig,
)
from moduslam.system_configs.frontend_manager.graph_builder.candidate_factory.config import (
    CandidateFactoryConfig,
)
from moduslam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from moduslam.system_configs.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)
from moduslam.system_configs.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)
from moduslam.system_configs.frontend_manager.handlers.lidar_odometry import (
    KissIcpScanMatcherConfig,
)
from moduslam.system_configs.setup_manager.edge_factories_initializer import (
    EdgeFactoriesInitializerConfig,
)
from moduslam.system_configs.setup_manager.handlers_factory import HandlersFactoryConfig
from moduslam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from moduslam.system_configs.setup_manager.sensors import Lidar3DConfig, SensorConfig
from moduslam.system_configs.setup_manager.setup_manager import SetupManagerConfig
from moduslam.system_configs.setup_manager.state_analyzers_factory import (
    StateAnalyzersFactoryConfig,
)
from tests.frontend_manager.handlers.scan_matchers.kiss_icp.scenarios import (
    el1,
    el2,
    sensor,
)

sensor_name: str = sensor.name
graph_builder_name: str = "lidar_map_builder"
handler_name: str = "kiss_icp_odometry"
handler_module_name: str = ".pointcloud_matcher"
handler_package_name: str = "moduslam.frontend_manager.handlers"
state_analyzer_name: str = "lidar_odometry_state_analyzer"
state_analyzer_module_name: str = ".lidar_odometry"
state_analyzer_package_name: str = "moduslam.frontend_manager.graph_builder.state_analyzers"
edge_factory_name: str = "lidar_odometry_edge_factory"
edge_factory_module_name: str = ".lidar_odometry"
edge_factory_package_name: str = "moduslam.frontend_manager.edge_factories"


@pytest.fixture
def elements() -> tuple[Element, Element]:
    return el1, el2


@pytest.fixture
def data_batch(elements) -> DataBatch:
    batch = DataBatch()
    for element in elements:
        batch.add(element)
    return batch


@pytest.fixture
def sensor_factory_cfg() -> SensorFactoryConfig:
    sensor_cfg: Lidar3DConfig = Lidar3DConfig(name=sensor_name)
    sensors: dict[str, SensorConfig] = {sensor_name: sensor_cfg}
    return SensorFactoryConfig(sensors)


@pytest.fixture
def handlers_factory_cfg() -> HandlersFactoryConfig:
    handler_cfg = KissIcpScanMatcherConfig(
        name=handler_name,
        type_name=ScanMatcher.__name__,
        module_name=handler_module_name,
    )
    return HandlersFactoryConfig(
        handlers={handler_name: handler_cfg},
        package_name=handler_package_name,
    )


@pytest.fixture
def edge_factories_initializer_cfg() -> EdgeFactoriesInitializerConfig:
    edge_factory_cfg = EdgeFactoryConfig(
        name=edge_factory_name,
        type_name=LidarOdometryEdgeFactory.__name__,
        module_name=edge_factory_module_name,
    )
    return EdgeFactoriesInitializerConfig(
        package_name=edge_factory_package_name,
        edge_factories={edge_factory_name: edge_factory_cfg},
    )


@pytest.fixture
def state_analyzers_factory_cfg():
    lidar_odometry_analyzer_cfg = StateAnalyzerConfig(
        name=state_analyzer_name,
        type_name=LidarOdometryStateAnalyzer.__name__,
        module_name=state_analyzer_module_name,
    )
    return StateAnalyzersFactoryConfig(
        package_name=state_analyzer_package_name,
        analyzers={state_analyzer_name: lidar_odometry_analyzer_cfg},
    )


@pytest.fixture
def setup_manager(
    sensor_factory_cfg,
    handlers_factory_cfg,
    edge_factories_initializer_cfg,
    state_analyzers_factory_cfg,
) -> SetupManager:
    config = SetupManagerConfig(
        sensors_factory=sensor_factory_cfg,
        handlers_factory=handlers_factory_cfg,
        edge_factories_initializer=edge_factories_initializer_cfg,
        state_analyzers_factory=state_analyzers_factory_cfg,
    )

    return SetupManager(config)


@pytest.fixture
def candidate_factory_cfg() -> CandidateFactoryConfig:
    return CandidateFactoryConfig(handler_state_analyzer_table={handler_name: state_analyzer_name})


@pytest.fixture
def distributor_cfg() -> ElementDistributorConfig:
    return ElementDistributorConfig(sensor_handlers_table={sensor_name: [handler_name]})


@pytest.fixture
def merger_cfg() -> GraphMergerConfig:
    return GraphMergerConfig(handler_edge_factory_table={handler_name: edge_factory_name})


@pytest.fixture
def builder_cfg(
    candidate_factory_cfg: CandidateFactoryConfig,
    distributor_cfg: ElementDistributorConfig,
    merger_cfg: GraphMergerConfig,
) -> GraphBuilderConfig:
    return GraphBuilderConfig(
        name=graph_builder_name,
        candidate_factory=candidate_factory_cfg,
        element_distributor=distributor_cfg,
        graph_merger=merger_cfg,
    )


@pytest.fixture
def builder(builder_cfg: GraphBuilderConfig, setup_manager) -> LidarMapBuilder:
    return LidarMapBuilder(builder_cfg)
