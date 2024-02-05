from abc import ABC, abstractmethod

from omegaconf import DictConfig

from slam.frontend_manager.elements_distributor.measurement_storage import Measurement


class Handler(ABC):
    """
    Base external module.
    """

    def __init__(self, config: DictConfig) -> None: ...

    @abstractmethod
    def process(self, element) -> Measurement | None: ...
