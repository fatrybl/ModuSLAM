"""
Tests description:

1) Create a dataset for a DataReader.
2) Initialize config files for DataReader
3) Initialize DataReader with config files.
4) Test methods:
    4.1) get_element()
    4.2) get_element(element[Element])
    4.3) get_element(sensor[Sensor])
    4.4) get_element(sensor[Sensor], timestamp[int])
"""

from pytest import raises

from configs.sensors.base_sensor_parameters import ParameterConfig
from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig
from configs.system.data_manager.batch_factory.regime import RegimeConfig
from slam.data_manager.factory.readers.element_factory import Element
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensors_factory.sensors import Encoder
from slam.utils.exceptions import FileNotValid
from tests.data_manager.factory.readers.kaist.api.empty_dataset.data import el1


class TestGetElement:
    """
    All test should raise FileNotValidException as KaistReader object cannot be initialized properly
    with empty '.csv' files. The Reader checks file validity before initializing files` iterators.
    """

    timestamp: int = 1
    sensor = Encoder("encoder", ParameterConfig())
    element: Element = el1

    def test_get_element_1(
        self,
        dataset_cfg: KaistConfig,
        regime_cfg: RegimeConfig,
    ):
        with raises(FileNotValid):
            reader = KaistReader(dataset_cfg, regime_cfg)
            reader.get_element()

    def test_get_element_2(self, dataset_cfg: KaistConfig, regime_cfg: RegimeConfig):
        with raises(FileNotValid):
            reader = KaistReader(dataset_cfg, regime_cfg)
            reader.get_element(self.element)

    def test_get_element_3(self, dataset_cfg: KaistConfig, regime_cfg: RegimeConfig):
        with raises(FileNotValid):
            reader = KaistReader(dataset_cfg, regime_cfg)
            reader.get_element(self.sensor)

    def test_get_element_4(self, dataset_cfg: KaistConfig, regime_cfg: RegimeConfig):
        with raises(FileNotValid):
            reader = KaistReader(dataset_cfg, regime_cfg)
            reader.get_element(self.sensor, self.timestamp)
