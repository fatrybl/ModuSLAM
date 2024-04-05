import pytest

from slam.data_manager.factory.element import Element
from slam.data_manager.factory.element import Measurement as RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.system_configs.system.frontend_manager.handlers.base_handler import (
    HandlerConfig,
)
from slam.utils.auxiliary_dataclasses import TimeRange


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
