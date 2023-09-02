"""
All custom exceptions
"""


class BatchFactoryException(Exception):
    "BatchFactory() has not been created"


class ConfigFileNotValid(OSError):
    'config file is not valid'
