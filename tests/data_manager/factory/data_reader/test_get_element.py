"""Tests for DataReader.get_element() methods. Implements readers from "description.txt"
file. All instances of DataReader should be tested here.

test_get_element_1 == get_element() test_get_element_2 == get_element(sensor: Sensor)
test_get_element_3 == get_element(element: Element) test_get_element_4 ==
get_element(sensor: Sensor, timestamp: int)
"""

import pytest

from slam.data_manager.factory.data_reader_ABC import DataReader
from slam.data_manager.factory.element import Element
from slam.setup_manager.sensors_factory.factory import SensorFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import (
    Stream,
    TimeLimit,
)
from slam.system_configs.system.setup_manager.sensors_factory import SensorFactoryConfig
from slam.utils.auxiliary_methods import equal_elements
from tests.data_manager.factory.data_reader.readers.kaist.case1 import kaist1
from tests.data_manager.factory.data_reader.readers.kaist.case2 import kaist2
from tests.data_manager.factory.data_reader.readers.kaist.case3 import kaist3
from tests.data_manager.factory.data_reader.readers.kaist.case4 import kaist4

test_cases_1 = (*kaist1,)
test_cases_2 = (*kaist2,)
test_cases_3 = (*kaist3,)
test_cases_4 = (*kaist4,)


class TestGetElement:

    @pytest.mark.parametrize(
        "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, reference_outputs",
        [*test_cases_1],
    )
    def test_get_element_1(
        self,
        sensor_factory_cfg: SensorFactoryConfig,
        dataset_cfg: DatasetConfig,
        regime: Stream | TimeLimit,
        data_reader_object: type[DataReader],
        reference_outputs: list[Element | None],
    ):
        SensorFactory.init_sensors(sensor_factory_cfg)

        data_reader = data_reader_object(regime=regime, dataset_params=dataset_cfg)

        for reference in reference_outputs:
            result: Element | None = data_reader.get_element()
            equal_elements(result, reference)

    @pytest.mark.parametrize(
        "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, inputs, reference_outputs",
        [*test_cases_2],
    )
    def test_get_element_2(
        self,
        sensor_factory_cfg: SensorFactoryConfig,
        dataset_cfg: DatasetConfig,
        regime: Stream | TimeLimit,
        data_reader_object: type[DataReader],
        inputs: list[Sensor],
        reference_outputs: list[Element | None],
    ):
        SensorFactory.init_sensors(sensor_factory_cfg)

        data_reader = data_reader_object(regime=regime, dataset_params=dataset_cfg)

        for sensor, reference in zip(inputs, reference_outputs):
            result: Element | None = data_reader.get_element(sensor)
            equal_elements(result, reference)

    @pytest.mark.parametrize(
        "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, inputs, reference_outputs",
        [*test_cases_3],
    )
    def test_get_element_3(
        self,
        sensor_factory_cfg: SensorFactoryConfig,
        dataset_cfg: DatasetConfig,
        regime: Stream | TimeLimit,
        data_reader_object: type[DataReader],
        inputs: list[Element],
        reference_outputs: list[Element | Exception],
    ):
        """get_element(element: Element) method ignores time regimes.

        It seeks for the element with the given sensor name and timestamp in the whole
        dataset.
        """
        SensorFactory.init_sensors(sensor_factory_cfg)

        data_reader = data_reader_object(regime=regime, dataset_params=dataset_cfg)

        for element, output in zip(inputs, reference_outputs):
            if isinstance(output, Exception):
                with pytest.raises(output.__class__):
                    data_reader.get_element(element)
            else:
                result: Element = data_reader.get_element(element)
                equal_elements(result, output)

    @pytest.mark.parametrize(
        "sensor_factory_cfg, dataset_cfg, regime, data_reader_object, inputs, reference_outputs",
        [*test_cases_4],
    )
    def test_get_element_4(
        self,
        sensor_factory_cfg: SensorFactoryConfig,
        dataset_cfg: DatasetConfig,
        regime: Stream | TimeLimit,
        data_reader_object: type[DataReader],
        inputs: list[tuple[Sensor, int]],
        reference_outputs: list[Element | Exception],
    ):
        """get_element(sensor: Sensor, timestamp: int) method ignores time regimes.

        It seeks for the element with the given sensor name and timestamp in the whole
        dataset.
        """
        SensorFactory.init_sensors(sensor_factory_cfg)

        data_reader = data_reader_object(regime=regime, dataset_params=dataset_cfg)

        for (sensor, timestamp), output in zip(inputs, reference_outputs):
            if isinstance(output, Exception):
                with pytest.raises(type(output)):
                    data_reader.get_element(sensor, timestamp)
            else:
                result: Element = data_reader.get_element(sensor, timestamp)
                equal_elements(result, output)
