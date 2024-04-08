import logging

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)

logger = logging.getLogger(__name__)


class State(MeasurementStorage):
    """State of the graph candidate."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def timestamp(self) -> int:
        """Time of the state.

        Raises:
            ValueError: if the start != stop timestamp of the time range.
        """
        return self.time_range.stop
