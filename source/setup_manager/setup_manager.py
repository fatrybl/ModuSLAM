from source.configs import DEFAULT_FILE_PATHS
from source.setup_manager import config, initializer

class SetupManager:
    def __init__(self) -> None:
        self.configs = {}

    def setup(self, objects: list) -> None:
        for object in objects:
            object_initializer = initializer(object)
            try:
                object_initializer.init()
            except: 
                Exception
            finally: 
                del object_initializer