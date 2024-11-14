"""Custom exceptions."""


class ItemNotFoundError(Exception):
    """The given item has not been found."""


class FileNotValid(Exception):
    """Invalid file: does not exist or is empty"""


class NotSubset(Exception):
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
