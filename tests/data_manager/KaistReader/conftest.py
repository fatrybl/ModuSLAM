from pytest import fixture

from shutil import rmtree, copyfile
from pathlib import Path

from tests.data_manager.KaistReader.data_factory import TestDataFactory
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader


@fixture(scope='module', autouse=False)
def prepare_data():
    data_factory = TestDataFactory()
    data_factory.prepare_data()
    data_factory.modify_default_config()
    yield


@fixture(scope='module', autouse=False)
def kaist_reader():
    yield KaistReader()


@fixture(scope='module', autouse=False)
def clean():
    yield
    copyfile(TestDataFactory.MODIFIED_DATAMANAGER_CONFIG_PATH,
             TestDataFactory.DEFAULT_DATAMANAGER_CONFIG_PATH)
    Path.unlink(TestDataFactory.MODIFIED_DATAMANAGER_CONFIG_PATH,
                missing_ok=True)
    rmtree(TestDataFactory.TEST_DATA_DIR)
