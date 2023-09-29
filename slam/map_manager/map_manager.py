import logging

class MapManager:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.map_saver = MapSaver()
        self.map_updater = MapUpdater()
        self.__map = Map()
        if self.config.attributes.smth:
            pass

    @property
    def map(self):
        pass

    def save_map() -> None:
        pass

    def update_map() -> None:
        pass
