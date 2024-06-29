"""Tests for DataReaderFactory.

Test cases:
1) Both dataset and regime configs are valid -> DataReader
2) Dataset config is invalid: incorrect name of the data reader -> NotImplementedError
3) Regime config is invalid: incorrect name of the regime -> ValueError
"""

from pytest import mark, raises

from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.data_reader_factory import (
    DataReaderFactory,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from tests.data_manager.batch_factory.data_reader_factory.scenarios import (
    scenario1,
    scenario2,
)

test_cases_1 = (*scenario1,)
test_cases_2 = (*scenario2,)


@mark.parametrize(
    "dataset_config, regime, reference_reader",
    [test_cases_1],
)
def test_get_reader(
    dataset_config: DatasetConfig,
    regime: Stream | TimeLimit,
    reference_reader: type[DataReader],
):
    reader = DataReaderFactory.create(dataset_config, regime)
    assert isinstance(reader, reference_reader)


@mark.parametrize(
    "dataset_config, regime",
    [test_cases_2],
)
def test_get_reader_invalid_dataset(dataset_config: DatasetConfig, regime: Stream | TimeLimit):
    with raises(NotImplementedError):
        DataReaderFactory.create(dataset_config, regime)
