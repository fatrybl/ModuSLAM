from slam.setup_manager.setup_manager import SetupManager
from slam.data_manager.data_manager import DataManager
from slam.frontend_manager.frontend_manager import FrontendManager
from slam.backend_manager.backend_manager import BackendManager
from slam.map_manager.map_manager import MapManager

import logging
# import slam.logger.logging_config


class MainManager:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.finished = False
        self.setup_manager = SetupManager()
        self.data_manager = DataManager()
        self.frontend_manager = FrontendManager()
        self.backend_manager = BackendManager()
        self.map_manager = MapManager()

    def build_map(self) -> None:
        while not self.finished:
            try:
                chunk = self.data_manager.make_chunk()

                self.frontend_manager.proccess(chunk)

                self.backend_manager.solve()

                self.map_manager.update_map()

            except Exception:
                pass

            finally:
                pass
