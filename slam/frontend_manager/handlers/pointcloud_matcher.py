from slam.data_manager.factory.element import Element
from slam.frontend_manager.handlers.ABC_handler import Handler


class PointcloudMatcher(Handler):
    def __init__(self, config) -> None:
        self._name = config.name

    def process(self, element: Element) -> None:
        pass

    @property
    def name(self) -> str:
        return self._name
