from pytest import fixture
from shutil import rmtree
from tests.data_manager.Ros1Reader.data_factory import TestDataFactory

@fixture(scope='module', autouse=True)
def prepare_data():
    data_factory = TestDataFactory()
    data_factory.prepare_data()
    yield


@fixture(scope='module', autouse=True)
def clean():
    yield
    rmtree(TestDataFactory.DATA_PATH_FOLDER.name)
    TestDataFactory.MASTER_FILE_PATH.unlink()



