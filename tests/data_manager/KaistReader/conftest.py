import pytest

from shutil import rmtree
from pathlib import Path

from tests.data_manager.KaistReader.data_factory import TestDataFactory


@pytest.fixture(scope='module', autouse=True)
def prepare_data():
    data_factory = TestDataFactory()
    data_factory.prepare_data()
    data_factory.modify_default_config()
    yield


@pytest.fixture(scope='function', autouse=True)
def clean():
    # Will be executed before the first test
    yield
    # Will be executed after the last test
    Path.unlink(TestDataFactory.DEFAULT_DATAMANAGER_CONFIG_PATH,
                missing_ok=True)
    Path.rename(TestDataFactory.MODIFIED_DATAMANAGER_CONFIG_PATH,
                TestDataFactory.DEFAULT_DATAMANAGER_CONFIG_PATH)

    rmtree(TestDataFactory.TEST_DATA_DIR)
