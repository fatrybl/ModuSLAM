from data_manager.data_manager import DataManager
from frontend_manager.frontend_manager import FrontendManager
from backend_manager.backend_manager import BackendManager
from map_manager.map_manager import MapManager
from utils.stopping_criterion import StoppingCriterion

import logging
# import slam.logger.logging_config


class MainManager:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.data_manager = DataManager()
        # self.frontend_manager = FrontendManager()
        # self.backend_manager = BackendManager()
        # self.map_manager = MapManager()

    def __process_batch(self):
        batch = self.data_manager.batch_factory.batch
        # while batch:
        #     self.frontend_manager.process(batch)
        #     self.backend_manager.solve()
        #     self.map_manager.update_map()

    def build_map(self) -> None:
        # while StoppingCriterion.OFF():

        self.data_manager.make_batch()

        self.__process_batch()
