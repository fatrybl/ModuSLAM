"""Test get_element() method for Kaist Urban Data Reader."""

from collections.abc import Iterable

from pytest import mark, raises

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from moduslam.data_manager.batch_factory.data_readers.kaist.reader import (
    KaistReader,
)
from moduslam.data_manager.batch_factory.utils import equal_elements
from moduslam.utils.exceptions import ItemNotFoundError
from tests.moduslam.data_manager.batch_factory.readers.kaist_urban.scenarios.case3 import (
    invalid_scenario,
    valid_scenarios,
)


@mark.parametrize("dataset_cfg, inputs, reference_elements", [*valid_scenarios])
def test_get_element_success(
    dataset_cfg: KaistConfig, inputs: Iterable[Element], reference_elements: Iterable[Element]
):
    reader = KaistReader(dataset_cfg)

    with reader:
        for element, reference_element in zip(inputs, reference_elements):
            result = reader.get_element(element)
            assert equal_elements(result, reference_element) is True


@mark.parametrize("dataset_cfg, invalid_elements", [invalid_scenario])
def test_get_element_invalid_element(dataset_cfg: KaistConfig, invalid_elements: Iterable[Element]):
    reader = KaistReader(dataset_cfg)

    with reader:
        for element in invalid_elements:
            with raises(ItemNotFoundError):
                reader.get_element(element)
