from abc import ABC, abstractmethod

from slam.data_manager.factory.readers.element_factory import Element


class ElementHandler(ABC):
    """
    Base external module.
    """

    @abstractmethod
    def process(self, element: Element):
        pass
