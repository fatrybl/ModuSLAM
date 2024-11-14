class SkipItemException(Exception):
    """Raise when a specific item should be skipped."""


class NotEnoughMeasurementsError(Exception):
    """Raise when not enough measurements are available."""
