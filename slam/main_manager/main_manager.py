import logging
import sys
import os
sys.path.insert(0, os.getcwd())
from slam.logger import logging_config

from slam.logger import logging_config
from slam.data_manager.data_manager import DataManager
from slam.frontend_manager.frontend_manager import FrontendManager
from slam.backend_manager.backend_manager import BackendManager
from slam.map_manager.map_manager import MapManager
from slam.utils.meta_singleton import MetaSingleton
from slam.utils.sensor_factory.factory import SensorFactory
from slam.utils.stopping_criterion import StoppingCriterionSingleton


logger = logging.getLogger(__name__)


class MainManager(metaclass=MetaSingleton):

    def __init__(self) -> None:
        self.break_point = StoppingCriterionSingleton()
        self.sensor_factory = SensorFactory()
        self.data_manager = DataManager()
        # self.frontend_manager = FrontendManager()
        # self.backend_manager = BackendManager()
        # self.map_manager = MapManager()
        logger.info("System has been successfully configured")

    def _process_batch(self) -> None:
        batch = self.data_manager.batch_factory.batch
        # while batch:
        #     self.frontend_manager.process(batch)
        #     self.backend_manager.solve()
        #     if loop_closure_criteria:
        #           self.frontend_manager._process_loops()
        #     self.map_manager.update_map()

    def build_map(self) -> None:
        logger.info("Building map...")
        while not self.break_point.ON:
            self.data_manager.make_batch()
            self._process_batch()

        logger.info("Map has been built")
