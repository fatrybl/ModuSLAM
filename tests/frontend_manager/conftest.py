"""Fixtures and classes for frontend_manager tests."""

from typing import Any, Callable, Iterable

import gtsam
import pytest

from slam.data_manager.factory.element import Element
from slam.data_manager.factory.element import RawMeasurement as RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.element_distributor.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
from slam.frontend_manager.graph.base_edges import UnaryEdge
from slam.frontend_manager.graph.base_vertices import Vertex
from slam.frontend_manager.graph.custom_vertices import Pose
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.system_configs.system.frontend_manager.handlers.base_handler import (
    HandlerConfig,
)
from slam.system_configs.system.setup_manager.sensors import SensorConfig
from slam.utils.auxiliary_dataclasses import TimeRange


class BasicTestHandler(Handler):

    def __init__(self, cfg: HandlerConfig):
        super().__init__(cfg)

    def process(self, element: Element) -> Measurement | None:
        m = create_measurement(self, element)
        return m


class BasicTestVertex(Vertex):
    def update(self, values: Any) -> None:
        pass


class BasicTestEdgeFactory(EdgeFactory):
    def __init__(self, config: EdgeFactoryConfig):
        super().__init__(config)

    @staticmethod
    def noise_model(values: Iterable[float]) -> Callable[[Iterable[float]], gtsam.noiseModel.Base]:
        return gtsam.noiseModel.Diagonal.Sigmas

    @property
    def vertices_types(self) -> set[type[Pose]]:
        return {Pose}

    @property
    def base_vertices_types(self) -> set[type[gtsam.Pose3]]:
        return {gtsam.Pose3}

    def create(self, graph, vertices, measurements) -> list[UnaryEdge]:
        f = gtsam.PriorFactorPoint2(
            key=0, prior=[0, 0], noiseModel=gtsam.noiseModel.Diagonal.Sigmas([1, 1])
        )
        noise = gtsam.noiseModel.Diagonal.Sigmas([1, 1])
        edge = UnaryEdge(vertex=BasicTestVertex(), measurements=(), noise_model=noise, factor=f)
        return [edge]


def create_measurement(handler: Handler, element: Element):
    return Measurement(
        time_range=TimeRange(element.timestamp, element.timestamp),
        values=element.measurement.values,
        handler=handler,
        elements=(element,),
        noise_covariance=(1, 1, 1),
    )


@pytest.fixture
def handler():
    cfg = HandlerConfig(
        name="test_handler", type_name=BasicTestHandler.__name__, module_name=__name__
    )
    handler = BasicTestHandler(cfg)
    return handler


@pytest.fixture
def sensor():
    cfg = SensorConfig(name="test_sensor", type_name="Sensor")
    return Sensor(config=cfg)


@pytest.fixture
def element(sensor) -> Element:
    loc = Location()
    m = RawMeasurement(sensor=sensor, values=(1, 2, 3))
    el = Element(timestamp=0, location=loc, measurement=m)
    return el


@pytest.fixture
def measurement(element, handler):
    return Measurement(
        time_range=TimeRange(element.timestamp, element.timestamp),
        values=(1, 2, 3),
        handler=handler,
        elements=(element,),
        noise_covariance=(1, 1, 1),
    )


@pytest.fixture
def measurement_storage(measurement):
    storage = MeasurementStorage()
    storage.add(measurement)
    return storage


@pytest.fixture
def edge_factory():
    cfg = EdgeFactoryConfig(
        name="test_edge_factory",
        type_name=BasicTestEdgeFactory.__name__,
        module_name=__name__,
        search_time_margin=1,
    )
    return BasicTestEdgeFactory(cfg)
