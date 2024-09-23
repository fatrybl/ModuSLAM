from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from moduslam.data_manager.batch_factory.batch import Element

if TYPE_CHECKING:
    from moduslam.frontend_manager.measurement_storage import Measurement


@runtime_checkable
class Handler(Protocol):
    def __init__(self, *args, **kwargs):
        """Initializes the handler.

        Args:
            config: configuration of the handler.
        """

    @property
    def name(self) -> str:
        """Unique name of the handler."""

    def process(self, element: Element) -> Measurement | None:
        """Processes the element.

        Args:
            element: element of a data batch to be processed.

        Returns:
            new measurement if created.
        """

    @staticmethod
    def create_empty_element(element: Element) -> Element:
        """Creates an empty element with the same timestamp, location and sensor as the
        input element. Must be used in every Handler.

        Args:
            element: element of a data batch with raw data.

        Returns:
            empty element without raw data.
        """
