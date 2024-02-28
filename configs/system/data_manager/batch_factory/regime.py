from abc import ABC
from dataclasses import dataclass


@dataclass
class RegimeConfig(ABC):
    """Abstract regime of data flow."""


@dataclass
class TimeLimitConfig(RegimeConfig):
    """Data flow is limited by time range."""

    start: int
    stop: int
    name: str = "TimeLimit"


@dataclass
class StreamConfig(RegimeConfig):
    """
    Free data flow: each measurement is processed sequentially.
    """

    name: str = "Stream"
