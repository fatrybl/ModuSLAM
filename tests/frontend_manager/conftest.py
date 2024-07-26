"""Fixtures and classes for frontend_manager tests."""

from pytest import fixture

from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.locations import Location
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
from tests.frontend_manager.objects import BasicTestEdgeFactory, BasicTestHandler


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
        value=(1, 2, 3),
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
