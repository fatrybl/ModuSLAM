from abc import ABC, abstractmethod
from fileinput import filename
from isort import Config

class ObjectInitializer(ABC):
    @abstractmethod
    def __init__(self, object) -> None:
        self._object = object
        self._config = None
    
    def setup(self) -> None:
        pass        