from pathlib2 import Path
from asdasdasd import DEFAULT_CFG_DIRECTORY_PATH
import logging

class SetupManager:
    logger = logging.getLogger(__name__)

    def __init__(self, cfg_directory_path = None) -> None:

        if cfg_directory_path:
            self.cfg_directory_path = Path(cfg_directory_path)
        else:
            self.cfg_directory_path = Path(DEFAULT_CFG_DIRECTORY_PATH)


    def setup(self, objects: list) -> None:
        for obj in objects:
            try:
                obj.setup()
            except: 
                Exception