"""
Custom exceptions
"""


class ConfigFileNotValid(OSError):
    'config file is not valid'


class FileNotValid(Exception):
    'invalid file'