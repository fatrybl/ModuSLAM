from pytest import mark, raises

from slam.data_manager.factory.data_reader_ABC import DataReader
from slam.data_manager.factory.data_reader_factory import DataReaderFactory
from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import RegimeConfig
from tests.data_manager.factory.data_reader_factory.scenarios import (
    scenario1,
    scenario2,
    scenario3,
)

test_cases_1 = (*scenario1,)
test_cases_2 = (*scenario2,)
test_cases_3 = (*scenario3,)


class TestDataReaderFactory:

    @mark.parametrize(
        "dataset_config, regime_config, reference_reader",
        [test_cases_1],
    )
    def test_get_reader(
        self,
        dataset_config: DatasetConfig,
        regime_config: RegimeConfig,
        reference_reader: type[DataReader],
    ):
        reader = DataReaderFactory.get_reader(dataset_config, regime_config)
        assert isinstance(reader, reference_reader)

    @mark.parametrize(
        "dataset_config, regime_config",
        [test_cases_2],
    )
    def test_get_reader_invalid_regime(
        self, dataset_config: DatasetConfig, regime_config: RegimeConfig
    ):
        with raises(ValueError):
            DataReaderFactory.get_reader(dataset_config, regime_config)

    @mark.parametrize(
        "dataset_config, regime_config",
        [test_cases_3],
    )
    def test_get_reader_invalid_dataset(
        self, dataset_config: DatasetConfig, regime_config: RegimeConfig
    ):
        with raises(NotImplementedError):
            DataReaderFactory.get_reader(dataset_config, regime_config)
