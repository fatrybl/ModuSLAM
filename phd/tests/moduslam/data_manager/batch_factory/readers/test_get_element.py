"""Tests for all overloads of get_element() method for any data reader.

 get_element (element: Element) -> Element:
    tests reading of specific element. Ignores time regimes.

Checklist:

| KaistReader | TumVieReader |             |
|-------------|--------------|--------------
|      +      |       +      |             |
|-------------|--------------|--------------
"""

import pytest
from pytest import mark

from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.configs import DatasetConfig
from phd.moduslam.data_manager.batch_factory.readers.reader_ABC import DataReader
from phd.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from phd.moduslam.data_manager.batch_factory.utils import equal_elements
from phd.moduslam.setup_manager.sensors_factory.configs import SensorConfig
from phd.moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from phd.tests.moduslam.data_manager.batch_factory.readers.test_cases.kaist.case3 import (
    kaist_invalid_element,
    kaist_out_of_context,
    kaist_success,
)
from phd.tests.moduslam.data_manager.batch_factory.readers.test_cases.tum_vie.case3 import (
    tum_vie_invalid_element,
    tum_vie_out_of_context,
    tum_vie_success,
)

test_cases_success = (*kaist_success, *tum_vie_success)
test_cases_invalid_element = (kaist_invalid_element, tum_vie_invalid_element)
test_cases_out_of_context = (kaist_out_of_context, tum_vie_out_of_context)


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, inputs, reference_elements",
    [*test_cases_success],
)
def test_get_element_success(
    sensor_factory_cfg: dict[str, SensorConfig],
    dataset_cfg: DatasetConfig,
    regime: Stream | TimeLimit,
    data_reader_object: type[DataReader],
    inputs: list[Element],
    reference_elements: list[Element],
):
    SensorsFactory.init_sensors(sensor_factory_cfg)
    reader = data_reader_object(regime, dataset_cfg)

    with reader:
        for element, reference_element in zip(inputs, reference_elements):
            result = reader.get_element(element)
            assert equal_elements(result, reference_element) is True


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, inputs, exceptions",
    [*test_cases_invalid_element],
)
def test_get_element_invalid_element(
    sensor_factory_cfg: dict[str, SensorConfig],
    dataset_cfg: DatasetConfig,
    regime: Stream | TimeLimit,
    data_reader_object: type[DataReader],
    inputs: list[Element],
    exceptions: list[type[Exception]],
):
    SensorsFactory.init_sensors(sensor_factory_cfg)
    reader = data_reader_object(regime, dataset_cfg)

    with reader:
        for element, exception in zip(inputs, exceptions):
            with pytest.raises(exception):
                reader.get_element(element)


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, input_element",
    [*test_cases_out_of_context],
)
def test_get_element_out_of_context(
    sensor_factory_cfg: dict[str, SensorConfig],
    dataset_cfg: DatasetConfig,
    regime: Stream | TimeLimit,
    data_reader_object: type[DataReader],
    input_element: Element,
):
    SensorsFactory.init_sensors(sensor_factory_cfg)
    reader = data_reader_object(regime, dataset_cfg)

    with pytest.raises(RuntimeError):
        reader.get_element(input_element)
