"""Custom exceptions."""


class ItemNotFoundError(Exception):
    """The given item has not been found."""


class ConfigFileNotValid(OSError):
    """Config file is not valid."""


class FileNotValid(Exception):
    """Invalid file: not exists or empty"""


class NotSubset(Exception):
    """The set is not a subset of another set."""


class ExternalModuleException(Exception):
    """External module failed to work properly."""


class DimensionalityError(Exception):
    """Invalid dimensions of an array."""
