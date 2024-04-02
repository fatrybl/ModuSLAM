import numpy as np
import pytest

from slam.data_manager.factory.element import Element
from slam.data_manager.factory.element import Measurement as RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.frontend_manager.element_distributor.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
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

    def process(self, element) -> Measurement | None: ...


@pytest.fixture
def elements() -> tuple[Element, ...]:
    loc = Location()
    cfg = SensorConfig(name="test_sensor", type_name="Sensor")
    s = Sensor(name="test_sensor", config=cfg)
    m1 = RawMeasurement(sensor=s, values=(1, 2, 3))
    m2 = RawMeasurement(sensor=s, values=(4, 5, 6))
    el1 = Element(timestamp=0, location=loc, measurement=m1)
    el2 = Element(timestamp=1, location=loc, measurement=m2)
    return el1, el2


@pytest.fixture
def handler():
    cfg = HandlerConfig(
        name="test_handler", type_name=BasicTestHandler.__name__, module_name=__name__
    )
    handler = BasicTestHandler(cfg)
    return handler


@pytest.fixture
def measurement(handler, elements):
    return Measurement(
        time_range=TimeRange(0, 1),
        values=np.array([1, 2, 3, 4, 5, 6]),
        handler=handler,
        elements=elements,
    )


class TestMeasurementStorage:
    def test_measurement_hashable(self, measurement):
        try:
            hash(measurement)
        except TypeError:
            pytest.fail("Measurement object is not hashable.")
        else:
            assert True

    def test_add_measurement(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        assert measurement in storage.data[measurement.handler]

    def test_add_data(self, measurement):
        storage = MeasurementStorage()
        data = {measurement.handler: OrderedSet([measurement])}
        storage.add(data)
        assert measurement in storage.data[measurement.handler]

    def test_remove(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        storage.remove(measurement)
        assert storage.is_empty

    def test_clear(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        storage.clear()
        assert storage.is_empty

    def test_recent_measurement(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        assert storage.recent_measurement == measurement

    def test_time_range(self, measurement):
        storage = MeasurementStorage()
        storage.add(measurement)
        assert storage.time_range == measurement.time_range
