from copy import deepcopy
import logging

from configs.main_config import Config

from slam.data_manager.factory.batch import DataBatch
from slam.logger import logging_config
from configs.main_config import Config
from slam.setup_manager.sensor_factory.sensors import Fog, Imu
from slam.setup_manager.setup_manager import SetupManager

from slam.data_manager.data_manager import DataManager
from slam.frontend_manager.frontend_manager import FrontendManager
from slam.backend_manager.backend_manager import BackendManager
from slam.map_manager.map_manager import MapManager
from slam.utils.auxiliary_dataclasses import PeriodicData, TimeRange
from slam.utils.meta_singleton import MetaSingleton
from slam.utils.stopping_criterion import StoppingCriterionSingleton


logger = logging.getLogger(__name__)

print(type(logger))


class MainManager(metaclass=MetaSingleton):

    def __init__(self, cfg: Config) -> None:
        self.break_point = StoppingCriterionSingleton()
        self.setup_manager = SetupManager(cfg.setup_manager)
        self.data_manager = DataManager(cfg.data_manager)
        # self.frontend_manager = FrontendManager()
        # self.backend_manager = BackendManager()
        # self.map_manager = MapManager()
        logger.info("The system has been successfully configured")

    def _process_batch(self) -> None:
        self.test_batch: DataBatch = deepcopy(
            self.data_manager.batch_factory.batch)
        for element in self.test_batch.data:
            element.measurement.values = None

    def create_batch_with_measurement(self):
        self.data_manager.make_batch(self.test_batch.data)

    # def create_batch_with_requests(self):
        # imu = Imu('imu', Path(
        #     '/home/oem/Desktop/PhD/mySLAM/configs/sensors/imu.yaml'))
        # fog = Fog('fog', Path(
        #     '/home/oem/Desktop/PhD/mySLAM/configs/sensors/fog.yaml'))

        # r1 = PeriodicData(imu, TimeRange(
        #     1544578498421679686, 1544578498441635438))
        # r2 = PeriodicData(fog, TimeRange(
        #     1544578498427683022, 1544578498429677931))
        # r3 = PeriodicData(fog, TimeRange(
        #     1544578498418649766, 1544578498420677814))
        # r4 = PeriodicData(imu, TimeRange(
        #     1544578498451636685, 1544578498471637525))
        # request = {r1, r2, r3, r4}
        # self.data_manager.make_batch(request)
        # print('finished')

    def validate(self):
        for element1, element2 in zip(self.test_batch.data, self.data_manager.batch_factory.batch.data):
            print('validating element')
            assert element1.location == element2.location
            assert element1.timestamp == element2.timestamp
            assert element1.measurement.sensor == element2.measurement.sensor

    def build_map(self) -> None:
        logger.info("Building map...")
        while not self.break_point.ON:
            self.data_manager.make_batch()
            self._process_batch()

        logger.info("Map has been built")
