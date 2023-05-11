class SetupManagerInitializer(Initializer):
    def __init__(self, object) -> None:
        super().__init__(object)
        self._config = Config("setup_manager.yaml")

    def setup(self) -> None:
        """some params for the object"""
        self._base_path = self._config.attributes('_____________')
        self._something_else = self._config.attributes('_________________')