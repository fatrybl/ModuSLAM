from abc import ABC, abstractmethod

class ObjectParameters(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass  