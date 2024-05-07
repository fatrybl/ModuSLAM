"""Simple handler for prior measurements.

Is used only for instantiation of the Measurement object.
"""

from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.frontend_manager.measurement_storage import Measurement


class PriorHandler(Handler):
    """Empty (fake) handler for prior measurements."""

    def __init__(self) -> None:
        self._name = "Prior Handler"

    def process(self, element) -> Measurement | None: ...
