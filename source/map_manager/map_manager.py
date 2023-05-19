import logging

class MapManager:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.map_saver = MapSaver()
        self.map_updater = MapUpdater()
    
    def setup(self):
        cfg = Config()

        if cfg.attributes.smth:
            self.smth = smth()

    def get_map(self) -> self.map:
        return self.map

    def save_map() -> None:
        pass

    def update_map() -> None:
        pass