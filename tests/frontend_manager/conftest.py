"""Fixtures and classes for frontend_manager tests."""

from typing import Any, Callable, Iterable

import gtsam
from pytest import fixture

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.locations import Location
from moduslam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from moduslam.frontend_manager.graph.base_edges import UnaryEdge
from moduslam.frontend_manager.graph.base_vertices import NotOptimizableVertex
from moduslam.frontend_manager.graph.custom_vertices import Pose
from moduslam.frontend_manager.handlers.ABC_handler import Handler
from moduslam.frontend_manager.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from moduslam.utils.auxiliary_dataclasses import TimeRange


class BasicTestHandler(Handler):

    def __init__(self, cfg: HandlerConfig):
        super().__init__(cfg)

    def process(self, element: Element) -> Measurement | None:
        m = create_measurement(self, element)
        return m

    def _create_empty_element(self, element: Element) -> Element:
        return element


class BasicTestVertex(NotOptimizableVertex):
    def update(self, value: Any) -> None:
        pass


class BasicTestEdgeFactory(EdgeFactory):
    def __init__(self, config: EdgeFactoryConfig):
        super().__init__(config)

    @staticmethod
    def noise_model() -> Callable[[Iterable[float]], gtsam.noiseModel.Base]:
        return gtsam.noiseModel.Diagonal.Sigmas

    @property
    def vertices_types(self) -> set[type[Pose]]:
        return {Pose}

    @property
    def base_vertices_types(self) -> set[type[gtsam.Pose3]]:
        return {gtsam.Pose3}

    def create(self, graph, measurements, timestamp: int) -> list[UnaryEdge]:
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


@fixture
def handler():
    cfg = HandlerConfig(
        name="test_handler", type_name=BasicTestHandler.__name__, module_name=__name__
    )
    handler = BasicTestHandler(cfg)
    return handler


@fixture
def sensor():
    cfg = SensorConfig(name="test_sensor", type_name="Sensor")
    return Sensor(config=cfg)


@fixture
def element(sensor) -> Element:
    loc = Location()
    m = RawMeasurement(sensor=sensor, values=(1, 2, 3))
    el = Element(timestamp=0, location=loc, measurement=m)
    return el


@fixture
def measurement(element, handler) -> Measurement:
    return Measurement(
        time_range=TimeRange(element.timestamp, element.timestamp),
        values=(1, 2, 3),
        handler=handler,
        elements=(element,),
        noise_covariance=(1, 1, 1),
    )


@fixture
def measurement_storage(measurement):
    storage = MeasurementStorage()
    storage.add(measurement)
    return storage


@fixture
def edge_factory():
    cfg = EdgeFactoryConfig(
        name="test_edge_factory",
        type_name=BasicTestEdgeFactory.__name__,
        module_name=__name__,
        search_time_margin=1,
    )
    return BasicTestEdgeFactory(cfg)
