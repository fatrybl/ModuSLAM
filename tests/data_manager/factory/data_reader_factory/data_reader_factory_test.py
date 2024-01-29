import pytest
from pytest import mark

from slam.data_manager.factory.readers.data_reader_ABC import DataReader
from slam.data_manager.factory.readers.data_reader_factory import DataReaderFactory
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

"""
Test description:
    checks if DataReaderFactory creates class object of correct type based on input dataset type.
"""


@mark.parametrize(("reader_name", "result"), [("KaistReader", KaistReader)])
def test_get_reader_success(reader_name: str, result: type[DataReader]):
    reader: type[DataReader] = DataReaderFactory.get_reader(reader_name)
    assert reader == result


@mark.parametrize(("reader_name", "exception"), [("UnknownReader", NotImplementedError)])
def test_get_reader_fail(reader_name: str, exception: Exception):
    with pytest.raises(exception):
        DataReaderFactory.get_reader(reader_name)
