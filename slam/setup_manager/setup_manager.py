from pathlib2 import Path
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
import logging

class SetupManager:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.cfg_directory= Path(ConfigFilePaths.cfg_directory_path.value)

    def setup(self, objects: list) -> None:
        for obj in objects:
            try:
                obj.setup()
            except: 
                Exception