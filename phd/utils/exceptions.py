"""Custom exceptions."""


class ValidationError(Exception):
    """Validations has failed."""


class ItemNotFoundError(Exception):
    """The item has not been found."""


class ItemExistsError(Exception):
    """The item already exists."""


class ItemNotExistsError(Exception):
    """The item does not exist."""


class FileNotValid(Exception):
    """Invalid file: does not exist or is empty"""


class NotSubsetError(Exception):
    """The set is not a subset of another set."""


class ExternalModuleException(Exception):
    """External module failed to work properly."""


class DimensionalityError(Exception):
    """Invalid dimensions of an array."""


class EmptyStorageError(Exception):
    """Raised when attempting to access an element of an empty storage."""


class EmptySensorsFactoryError(EmptyStorageError):
    """The sensors factory is empty."""


class DataReaderConfigurationError(Exception):
    """Invalid data reader configuration."""


class ClosedSourceError(Exception):
    """Raised when attempting to access a source that is closed."""


class StateNotSetError(Exception):
    """The state has not been set."""


class UnfeasibleRequestError(Exception):
    """The request is unfeasible."""


class SkipItemException(Exception):
    """Raise when a specific item should be skipped."""


class NotEnoughMeasurementsError(Exception):
    """Raise when not enough measurements are available."""
