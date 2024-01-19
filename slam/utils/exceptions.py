"""
Custom exceptions
"""


class ConfigFileNotValid(OSError):
    "config file is not valid"


class FileNotValid(Exception):
    "Invalid file: not exists or empty"


class NotSubset(Exception):
    "if a set is not a subset of another set"


class SensorNotFound(Exception):
    "Sensor has not been found"


class ExternalModuleException(Exception):
    "External module failed to work properly"
