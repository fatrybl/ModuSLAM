from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.handlers.ABC_handler import Handler


class ImuPreintegration(Handler):
    def __init__(self) -> None:
        pass

    def process(self, element) -> Measurement | None: ...
