from abc import ABC, abstractmethod

from configs.system.frontend_manager.handlers.base_handler import HandlerConfig
from slam.frontend_manager.element_distributor.measurement_storage import Measurement


class Handler(ABC):
    """
    Base external module.
    """

    @abstractmethod
    def __init__(self, config: HandlerConfig) -> None:
        self._name = config.name
        self._parameters = config.parameters

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def process(self, element) -> Measurement | None: ...
