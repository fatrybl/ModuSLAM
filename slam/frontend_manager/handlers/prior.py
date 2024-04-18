"""Simple handler for prior measurements.

Is used only for instantiation of the Measurement object.
"""

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.handlers.ABC_handler import Handler


class PriorHandler(Handler):
    """Handler for prior measurements."""

    def __init__(self) -> None:
        self._name = "Prior Handler"

    def process(self, element) -> Measurement | None: ...
