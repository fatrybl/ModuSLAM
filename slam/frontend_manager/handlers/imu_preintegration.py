from system_configs.system.frontend_manager.handlers.base_handler import HandlerConfig

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.handlers.ABC_handler import Handler


class ImuPreintegration(Handler):
    """IMU preintegration handler."""

    def __init__(self, config: HandlerConfig) -> None:
        self._name: str = config.name

    @property
    def name(self) -> str:
        return self._name

    def process(self, element) -> Measurement | None: ...
