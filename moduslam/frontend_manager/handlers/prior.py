"""Simple handler for prior measurements.

Is used only for instantiation of the Measurement object.
"""

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.handlers.ABC_handler import Handler
from moduslam.frontend_manager.measurement_storage import Measurement


class PriorHandler(Handler):
    """Empty (fake) handler for prior measurements."""

    def __init__(self) -> None:
        self._name = "Prior Handler"

    def process(self, element) -> Measurement | None: ...

    def _create_empty_element(self, element: Element) -> Element:
        raise NotImplementedError
