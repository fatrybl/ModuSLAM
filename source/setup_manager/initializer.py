from abc import ABC, abstractmethod

class Initializer(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass