"""Tests for the ElementDistributor class."""

from unittest.mock import patch

import pytest

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.element import Element
from slam.data_manager.factory.element import Measurement as RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.frontend_manager.element_distributor.elements_distributor import (
    ElementDistributor,
)
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.frontend_manager.handlers.base_handler import (
    HandlerConfig,
)
from slam.system_configs.system.setup_manager.sensors_factory import SensorConfig
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.ordered_set import OrderedSet


class BasicTestHandler(Handler):

    def __init__(self, cfg: HandlerConfig):
        super().__init__(cfg)

    def process(self, element: Element) -> Measurement | None:
        m = create_measurement(self, element)
        return m


def create_measurement(handler: BasicTestHandler, element: Element):
    return Measurement(
        time_range=TimeRange(element.timestamp, element.timestamp),
        values=element.measurement.values,
        handler=handler,
        elements=(element,),
    )


@pytest.fixture
def handler():
    cfg = HandlerConfig(
        name="test_handler", type_name=BasicTestHandler.__name__, module_name=__name__
    )
    handler = BasicTestHandler(cfg)
    return handler


@pytest.fixture
def element(sensor) -> Element:
    loc = Location()
    m = RawMeasurement(sensor=sensor, values=(1, 2, 3))
    el = Element(timestamp=0, location=loc, measurement=m)
    return el


@pytest.fixture
def sensor():
    cfg = SensorConfig(name="test_sensor", type_name="Sensor")
    return Sensor(name="test_sensor", config=cfg)


@pytest.fixture
def data_batch(element: Element) -> DataBatch:
    db = DataBatch()
    db.add(element)
    return db


def test_distribute_next(data_batch, sensor, handler):
    table = {sensor: [handler]}
    measurement = create_measurement(handler, data_batch.first)
    element_distributor = ElementDistributor()

    with patch.object(ElementDistributor, "sensor_handler_table", table):

        element_distributor.distribute_next(data_batch)
        assert measurement in element_distributor.storage.data[handler]


def test_clear_storage(handler, element):
    element_distributor = ElementDistributor()
    measurement = create_measurement(handler, element)
    element_distributor.storage.add(measurement)

    assert measurement in element_distributor.storage.data[handler]

    element_distributor.clear_storage([OrderedSet([measurement])])

    assert element_distributor.storage.is_empty
