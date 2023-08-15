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
from slam.utils.stopping_criterion import StoppingCriterionSingleton


logger = logging.getLogger(__name__)


class MainManager:

    def __init__(self) -> None:
        self.data_manager = DataManager()
        # self.frontend_manager = FrontendManager()
        # self.backend_manager = BackendManager()
        # self.map_manager = MapManager()
        self.__break_point = StoppingCriterionSingleton()
        logger.info("System has been successfully configured")

    def __process_batch(self) -> None:
        batch = self.data_manager.batch_factory.batch
        # while batch:
        #     self.frontend_manager.process(batch)
        #     self.backend_manager.solve()
        #     self.map_manager.update_map()

    def build_map(self) -> None:
        while not self.__break_point.ON:
            logger.info("Building map...")
            self.data_manager.make_batch()
            self.__process_batch()

        logger.info("Map has been built")
