from pytest import fixture
from shutil import rmtree
from tests.data_manager.Ros1Reader.data_factory import TestDataFactory
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from configs.experiments.ros1.config import Ros1, Sensors

@fixture(scope='module', autouse=True)
def prepare_data():
    data_factory = TestDataFactory()
    data_factory.prepare_data()
    cfg = Sensors()
    SensorFactory(cfg)
    yield


@fixture(scope='module', autouse=True)
def clean():
    yield
    rmtree(TestDataFactory.DATA_PATH_FOLDER.name)
    TestDataFactory.MASTER_FILE_PATH.unlink()



