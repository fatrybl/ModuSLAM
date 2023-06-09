import logging
from utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths


class MapManager:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.map_saver = MapSaver()
        self.map_updater = MapUpdater()
        self.__map = Map()
        self.config = Config(ConfigFilePaths.map_manager_config)
        if self.config.attributes.smth:
            pass

    @property
    def map(self) -> Map:
        return self.__map

    def save_map() -> None:
        pass

    def update_map() -> None:
        pass
