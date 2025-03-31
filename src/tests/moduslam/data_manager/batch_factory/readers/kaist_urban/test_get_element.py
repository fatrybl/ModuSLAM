"""Test get_element() method for Kaist Urban Data Reader."""

from pytest import mark, raises

from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.kaist.reader import (
    KaistReader,
)
from src.moduslam.data_manager.batch_factory.utils import equal_elements
from src.tests.moduslam.data_manager.batch_factory.readers.kaist_urban.data.case3 import (
    invalid_scenario,
    out_of_context,
    valid_scenarios,
)


@mark.parametrize("dataset_cfg, inputs, reference_elements", [*valid_scenarios])
def test_get_element_success(
    dataset_cfg: KaistConfig, inputs: list[Element], reference_elements: list[Element]
):
    reader = KaistReader(dataset_cfg)

    with reader:
        for element, reference_element in zip(inputs, reference_elements):
            result = reader.get_element(element)
            assert equal_elements(result, reference_element) is True


@mark.parametrize("dataset_cfg, inputs, exceptions", [invalid_scenario])
def test_get_element_invalid_element(
    dataset_cfg: KaistConfig, inputs: list[Element], exceptions: list[type[Exception]]
):
    reader = KaistReader(dataset_cfg)

    with reader:
        for element, exception in zip(inputs, exceptions):
            with raises(exception):
                reader.get_element(element)


@mark.parametrize("dataset_cfg, input_element", [out_of_context])
def test_get_element_out_of_context(dataset_cfg: KaistConfig, input_element: Element):
    reader = KaistReader(dataset_cfg)

    with raises(RuntimeError):
        reader.get_element(input_element)
