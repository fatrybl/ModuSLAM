"""Tests for all overloads of get_element() method for any data reader.

 get_element (element: Element) -> Element:
    tests reading of specific element. Ignores time regimes.

Checklist:

| KaistReader | TumVieReader |             |
|-------------|--------------|--------------
|      +      |       +      |             |
|-------------|--------------|--------------
"""

from pytest import mark, raises

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from moduslam.system_configs.setup_manager.sensor_factory import SensorsFactoryConfig
from moduslam.utils.auxiliary_methods import equal_elements
from tests.data_manager.batch_factory.readers.test_cases.kaist.case3 import (
    kaist_fail,
    kaist_success,
)
from tests.data_manager.batch_factory.readers.test_cases.tum_vie.case3 import (
    tum_vie_fail,
    tum_vie_success,
)

test_cases_success = (*kaist_success, *tum_vie_success)
test_cases_fail = (*kaist_fail, *tum_vie_fail)


@mark.parametrize(
    "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, inputs, reference_elements",
    [*test_cases_success],
)
def test_get_element_success(
    sensor_factory_cfg: SensorsFactoryConfig,
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
    [*test_cases_fail],
)
def test_get_element_fail(
    sensor_factory_cfg: SensorsFactoryConfig,
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
            with raises(exception):
                reader.get_element(element)
