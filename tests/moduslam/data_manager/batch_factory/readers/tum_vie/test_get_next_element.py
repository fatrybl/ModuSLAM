"""Tests for overloads of get_next_element() method for TUM VIE Data Reader.

The DataReader must work in 2 regimes: Stream and TimeLimit,
get_next_element() should be tested for both of them.

1. get_next_element() -> Element | None:
    tests sequential reading of elements.

2. get_next_element_of_sensor() -> Element | None:
    tests sequential reading of sensor-specific elements.
"""

from collections.abc import Iterable

from pytest import mark

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from moduslam.data_manager.batch_factory.data_readers.tum_vie.reader import (
    TumVieReader,
)
from moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.data_manager.batch_factory.utils import equal_elements
from moduslam.sensors_factory.configs import SensorConfig
from moduslam.sensors_factory.factory import SensorsFactory
from moduslam.sensors_factory.sensors import Sensor
from tests.moduslam.data_manager.batch_factory.readers.tum_vie.scenarios.case1 import (
    tum_vie1,
)
from tests.moduslam.data_manager.batch_factory.readers.tum_vie.scenarios.case2 import (
    tum_vie2,
)


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, reference_outputs",
    [*tum_vie1],
)
def test_get_next_element(
    sensor_factory_cfg: Iterable[SensorConfig],
    dataset_cfg: TumVieConfig,
    regime: Stream | TimeLimit,
    reference_outputs: Iterable[Element | None],
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
    "sensor_factory_cfg, dataset_cfg, regime, sensors, reference_outputs",
    [*tum_vie2],
)
def test_get_next_element_of_sensor(
    sensor_factory_cfg: Iterable[SensorConfig],
    dataset_cfg: TumVieConfig,
    regime: Stream | TimeLimit,
    sensors: Iterable[Sensor],
    reference_outputs: Iterable[Element | None],
):
    SensorsFactory.init_sensors(sensor_factory_cfg)
    all_sensors = SensorsFactory.get_sensors()
    reader = TumVieReader(dataset_cfg)
    reader.configure(regime, all_sensors)

    with reader:
        for sensor, reference in zip(sensors, reference_outputs):
            result = reader.get_next_element(sensor)
            assert equal_elements(result, reference) is True
