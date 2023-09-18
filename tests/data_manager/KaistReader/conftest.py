from pytest import fixture

from shutil import rmtree, copyfile, copytree
from pathlib import Path
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory

from tests.data_manager.KaistReader.data_factory import TestDataFactory
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader


@fixture(scope='module', autouse=True)
def prepare_data():
    data_factory = TestDataFactory()
    data_factory.prepare_data()
    data_factory.modify_default_config()
    SensorFactory()
    yield


@fixture(scope='module', autouse=False)
def kaist_reader():
    yield KaistReader()


@fixture(scope='module', autouse=True)
def clean():
    yield
    copyfile(TestDataFactory.MODIFIED_DATAMANAGER_CONFIG_PATH,
             TestDataFactory.DEFAULT_DATAMANAGER_CONFIG_PATH)
    Path.unlink(TestDataFactory.MODIFIED_DATAMANAGER_CONFIG_PATH,
                missing_ok=True)

    rmtree(TestDataFactory.DEFAULT_SENSORS_CONFIG_DIR)
    copytree(TestDataFactory.MODIFIED_SENSORS_CONFIG_DIR,
             TestDataFactory.DEFAULT_SENSORS_CONFIG_DIR)

    rmtree(TestDataFactory.MODIFIED_SENSORS_CONFIG_DIR)
    rmtree(TestDataFactory.TEST_DATA_DIR)
