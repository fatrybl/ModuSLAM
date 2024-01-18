import pytest
from pytest import mark
from typing import Type

from hydra import compose, initialize_config_module

from slam.data_manager.factory.readers.data_reader_factory import DataReaderFactory
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

"""
Test description:
    checks if DataReaderFactory creates data reader object of correct type based on input dataset type.
"""


@mark.parametrize(("overrides", "result"), [(["type=Kaist"], KaistReader)])
def test_DataReaderFactory_success(overrides: list[str], result: Type[DataReader]):
    with initialize_config_module(config_module="data_reader_factory.conf"):
        cfg = compose(config_name="config", overrides=overrides)
        dataset_type: str = cfg.type
        factory = DataReaderFactory(dataset_type)
        reader = factory.data_reader
        assert reader == result


@mark.parametrize(("overrides", "exception"), [(["type=SomeUnsupportedType"], NotImplementedError)])
def test_DataReaderFactory_exception(overrides: list[str], exception: Type[Exception]):
    with initialize_config_module(config_module="data_reader_factory.conf"):
        cfg = compose(config_name="config", overrides=overrides)
        dataset_type: str = cfg.type
        with pytest.raises(exception):
            DataReaderFactory(dataset_type)
