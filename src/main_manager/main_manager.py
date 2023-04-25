from src.setup_manager import SetupManager
from src.data_manager import DataManager
from src.frontend_manager import FrontendManager
from src.backend_manager import BackendManager
from src.map_manager import MapManager

class MainManager:
    def __init__(self) -> None:
        setup_manager = SetupManager()
        data_manager = DataManager()
        frontend_manager = FrontendManager()
        backend_manager = BackendManager()
        map_manager = MapManager()
        logger = Logger()

    def build_map() ->  None:
        try:
            setup_manager.setup_system()
        except "SetumManagerException"

        try: 
            data_manager.make_data_chunk()
        except: "DataManagerException"

        try: 
            frontend_manager.proccess_data_chunk()
        except: "FrontendManagerException"

        try: 
            frontend_manager.add_factors()
        except: "FrontendManagerException"

        try:
            backend_manager.solve_graph()
        except: "BackendManagerException"

        try: 
            map_manager.update_map()
        except: "MapManagerException"

        finally:
            pass