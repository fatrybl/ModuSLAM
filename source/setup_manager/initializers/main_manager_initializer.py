class MainManagerInitializer(ObjectInitializer):
    def __init__(self, object) -> None:
        super().__init__(object)
        self._config = Config("main_manager.yaml")

    def setup(self) -> None:
        """some params for the object"""
        self._object.name = self._config.attributes('name')
        self._object.description = self._config.attributes('description')
        self._object.version = self._config.attributes('version')