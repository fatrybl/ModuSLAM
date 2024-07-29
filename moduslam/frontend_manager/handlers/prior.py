"""Simple handler for prior measurements.

Is used only for instantiation of the Measurement object.
"""

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.handlers.interface import Handler
from moduslam.frontend_manager.measurement_storage import Measurement


class PriorHandler(Handler):
    """Empty (fake) handler for prior measurements."""

    def __init__(self): ...

    @property
    def name(self) -> str:
        """Unique handler name."""
        return "Prior Handler"

    def process(self, element) -> Measurement | None: ...

    @staticmethod
    def create_empty_element(element: Element) -> Element:
        raise NotImplementedError
