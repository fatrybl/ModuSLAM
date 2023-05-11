from source.configs.paths import DEFAULT_FILE_PATHS
from source.setup_manager import config
from source.setup_manager.initializers import initializer

class SetupManager:
    def __init__(self) -> None:
        self.initializer = SetupManagerInitializer(self)
        self._base_path = None
        self._something_else = None

    @staticmethod
    def setup(objects: list) -> None:
        assert len(objects) > 0

        for object in objects:
            try:
                object.initializer.setup()
            except: 
                Exception