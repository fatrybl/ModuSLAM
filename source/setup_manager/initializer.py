from abc import ABC, abstractmethod

class Initializer(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._config = None
        self._object_type = None
        

class SetupManagerInitializer(Initializer):
    pass

class MainManagerInitializer(Initializer):
    pass

class FrontendManagerInitializer(Initializer):
    pass

class BackendManagerInitializer(Initializer):
    pass

class DataManagerInitializer(Initializer):
    pass