from source.setup_manager import SetupManager
from source.data_manager import DataManager
from source.frontend_manager import FrontendManager
from source.backend_manager import BackendManager
from source.map_manager import MapManager
import logging


class MainManager:
    def __init__(self) -> None:
        self.finished = False
        self.setup_manager = SetupManager()
        self.data_manager = DataManager()
        self.frontend_manager = FrontendManager()
        self.backend_manager = BackendManager()
        self.map_manager = MapManager()
        self.main_logger = logging.getLogger(__name__)

    def setup_system(self) -> None:
        objects = [self.data_manager, 
                   self.frontend_manager, 
                   self.backend_manager, 
                   self.map_manager, 
                   self.main_logger]
        try:
            self.setup_manager.setup(objects)

        except SomeException:
            self.main_logger.error("Setup failed")


    def build_map(self) ->  None:
        while not self.finished:
            try: 
                chunk = self.data_manager.make_data_chunk()

                self.frontend_manager.proccess_data_chunk(chunk)

                self.backend_manager.solve_problem()

                self.map_manager.update_map()

            except Exception: pass

            finally:
                pass