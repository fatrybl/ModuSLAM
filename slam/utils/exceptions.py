"""
Custom exceptions
"""


class ConfigFileNotValid(OSError):
    'config file is not valid'


class FileNotValid(Exception):
    'invalid file'


class NotSubset(Exception):
    'if a set is not a subset of another set'

class TopicNotFound(Exception):
    'no such topic in file'


class SensorNotFound(Exception):
    'Sensor has not benn found'

