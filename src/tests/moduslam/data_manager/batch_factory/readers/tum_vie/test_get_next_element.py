"""Tests for overloads of get_next_element() method for TUM VIE Data Reader.

The DataReader must work in 2 regimes: Stream and TimeLimit,
get_next_element() should be tested for both of them.

1. get_next_element() -> Element | None:
    tests sequential reading of elements.

2. get_next_element_of_sensor() -> Element | None:
    tests sequential reading of sensor-specific elements.
"""

from pytest import mark

from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.reader import (
    TumVieReader,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.data_manager.batch_factory.utils import equal_elements
from src.moduslam.sensors_factory.configs import SensorConfig
from src.moduslam.sensors_factory.factory import SensorsFactory
from src.moduslam.sensors_factory.sensors import Sensor
from src.tests.moduslam.data_manager.batch_factory.readers.tum_vie.data.case1 import (
    tum_vie1,
)
from src.tests.moduslam.data_manager.batch_factory.readers.tum_vie.data.case2 import (
    tum_vie2,
)


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, reference_outputs",
    [*tum_vie1],
)
def test_get_next_element(
    sensor_factory_cfg: dict[str, SensorConfig],
    dataset_cfg: TumVieConfig,
    regime: Stream | TimeLimit,
    reference_outputs: list[Element | None],
):
    SensorsFactory.init_sensors(sensor_factory_cfg)
    sensors = SensorsFactory.get_sensors()
    reader = TumVieReader(dataset_cfg)
    reader.configure(regime, sensors)

    with reader:
        for reference in reference_outputs:
            result = reader.get_next_element()
            assert equal_elements(result, reference) is True


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, inputs, reference_outputs",
    [*tum_vie2],
)
def test_get_next_element_of_sensor(
    sensor_factory_cfg: dict[str, SensorConfig],
    dataset_cfg: TumVieConfig,
    regime: Stream | TimeLimit,
    inputs: list[Sensor],
    reference_outputs: list[Element | None],
):
    SensorsFactory.init_sensors(sensor_factory_cfg)
    sensors = SensorsFactory.get_sensors()
    reader = TumVieReader(dataset_cfg)
    reader.configure(regime, sensors)

    with reader:
        for sensor, reference in zip(inputs, reference_outputs):
            result = reader.get_next_element(sensor)
            assert equal_elements(result, reference) is True
