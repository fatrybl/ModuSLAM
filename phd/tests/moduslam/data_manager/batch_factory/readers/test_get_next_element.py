"""Tests for all overloads of get_next_element() method for any data reader.

Any DataReader must work in 2 regimes: Stream and TimeLimit,
get_next_element() should be tested for both of them.

1. get_next_element() -> Element | None:
    tests sequential reading of elements in different regimes.

2. get_next_element_of_sensor() -> Element | None:
    tests sequential reading of sensor`s elements in different regimes.

Checklist:

| Overload  | KaistReader | TumVieReader |             |
------------|-------------|--------------|--------------
| 1         |     +       |              |             |
------------|-------------|--------------|--------------
| 2         |     +       |              |             |
------------|-------------|--------------|--------------
"""

from pytest import mark

from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.configs import DatasetConfig
from phd.moduslam.data_manager.batch_factory.readers.reader_ABC import DataReader
from phd.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from phd.moduslam.data_manager.batch_factory.utils import equal_elements
from phd.moduslam.sensors_factory.configs import SensorConfig
from phd.moduslam.sensors_factory.factory import SensorsFactory
from phd.moduslam.sensors_factory.sensors import Sensor
from phd.tests.moduslam.data_manager.batch_factory.readers.test_cases.kaist.case1 import (
    kaist1,
)
from phd.tests.moduslam.data_manager.batch_factory.readers.test_cases.kaist.case2 import (
    kaist2,
)
from phd.tests.moduslam.data_manager.batch_factory.readers.test_cases.tum_vie.case1 import (
    tum_vie1,
)
from phd.tests.moduslam.data_manager.batch_factory.readers.test_cases.tum_vie.case2 import (
    tum_vie2,
)

test_cases_1 = (*kaist1, *tum_vie1)
test_cases_2 = (*kaist2, *tum_vie2)


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, reference_outputs",
    [*test_cases_1],
)
def test_get_next_element(
    sensor_factory_cfg: dict[str, SensorConfig],
    dataset_cfg: DatasetConfig,
    regime: Stream | TimeLimit,
    data_reader_object: type[DataReader],
    reference_outputs: list[Element | None],
):
    SensorsFactory.init_sensors(sensor_factory_cfg)
    reader = data_reader_object(regime, dataset_cfg)

    with reader:
        for reference in reference_outputs:
            result = reader.get_next_element()
            assert equal_elements(result, reference) is True


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, inputs, reference_outputs",
    [*test_cases_2],
)
def test_get_next_element_of_sensor(
    sensor_factory_cfg: dict[str, SensorConfig],
    dataset_cfg: DatasetConfig,
    regime: Stream | TimeLimit,
    data_reader_object: type[DataReader],
    inputs: list[Sensor],
    reference_outputs: list[Element | None],
):
    SensorsFactory.init_sensors(sensor_factory_cfg)
    reader = data_reader_object(regime, dataset_cfg)

    with reader:
        for sensor, reference in zip(inputs, reference_outputs):
            result = reader.get_next_element(sensor)
            assert equal_elements(result, reference) is True
