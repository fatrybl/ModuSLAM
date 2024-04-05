import pytest

from slam.data_manager.factory.element import Element
from slam.data_manager.factory.element import Measurement as RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.system_configs.system.frontend_manager.handlers.base_handler import (
    HandlerConfig,
)
from slam.system_configs.system.setup_manager.sensors_factory import SensorConfig
from slam.utils.auxiliary_dataclasses import TimeRange


class BasicTestHandler(Handler):

    def __init__(self, cfg: HandlerConfig):
        super().__init__(cfg)

    def process(self, element: Element) -> Measurement | None:
        m = measurement(element, self)
        return m


@pytest.fixture
def state_analyzer_config():
    return StateAnalyzerConfig(
        name="test_state_analyzer",
        handler_name="test_handler",
        type_name="test_type",
        module_name="test_module",
    )


@pytest.fixture
def state_analyzer(state_analyzer_config):
    return LidarOdometryStateAnalyzer(state_analyzer_config)


@pytest.fixture
def handler():
    cfg = HandlerConfig(
        name="test_handler", type_name=BasicTestHandler.__name__, module_name=__name__
    )
    handler = BasicTestHandler(cfg)
    return handler


@pytest.fixture
def element():
    cfg = SensorConfig(name="test_sensor", type_name=Sensor.__name__)
    m = RawMeasurement(
        sensor=Sensor(config=cfg),
        values=(1, 2, 3),
    )
    return Element(timestamp=0, measurement=m, location=Location())


@pytest.fixture
def measurement(element, handler):
    return Measurement(
        time_range=TimeRange(element.timestamp, element.timestamp),
        values=(1, 2, 3),
        handler=handler,
        elements=(element,),
    )
