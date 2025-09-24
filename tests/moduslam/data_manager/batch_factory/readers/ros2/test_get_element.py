"""Test get_element() method for Ros-2 Data Reader."""

from collections.abc import Iterable

from pytest import mark, raises

from moduslam.data_manager.batch_factory.data_objects import Element
from moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2Config,
)
from moduslam.data_manager.batch_factory.data_readers.ros2.reader import Ros2Reader
from moduslam.data_manager.batch_factory.utils import equal_elements
from moduslam.utils.exceptions import ItemNotFoundError
from tests.moduslam.data_manager.batch_factory.readers.ros2.scenarios.case3 import (
    invalid_scenarios,
    valid_scenarios,
)


@mark.parametrize("dataset_cfg, inputs, reference_elements", [*valid_scenarios])
def test_get_element_success(
    dataset_cfg: Ros2Config, inputs: Iterable[Element], reference_elements: Iterable[Element]
):
    reader = Ros2Reader(dataset_cfg)

    with reader:
        for element, reference_element in zip(inputs, reference_elements):
            result = reader.get_element(element)
            assert equal_elements(result, reference_element) is True


@mark.parametrize("dataset_cfg, invalid_elements", [*invalid_scenarios])
def test_get_element_invalid_element(dataset_cfg: Ros2Config, invalid_elements: Iterable[Element]):
    reader = Ros2Reader(dataset_cfg)

    with reader:
        for element in invalid_elements:
            with raises(ItemNotFoundError):
                reader.get_element(element)
