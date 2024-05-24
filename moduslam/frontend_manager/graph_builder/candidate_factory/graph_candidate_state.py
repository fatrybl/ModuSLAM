from moduslam.frontend_manager.measurement_storage import MeasurementStorage


class State(MeasurementStorage):
    """State of the storage with measurements in exact time moment.

    Used for the graph candidate.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def timestamp(self) -> int:
        """Time stamp of the state."""
        return self.time_range.stop
