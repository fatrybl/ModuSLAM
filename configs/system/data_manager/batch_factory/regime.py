from abc import ABC
from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class RegimeConfig(ABC):
    """
    Abstract regime of data flow.
    """

    name: str = MISSING


@dataclass
class TimeLimitConfig(RegimeConfig):
    """
    Data flow is limited by time range.
    """

    start: int = MISSING
    stop: int = MISSING
    name: str = "TimeLimit"


@dataclass
class StreamConfig(RegimeConfig):
    """
    Free data flow: each measurement is processed sequantially.
    """

    name: str = "Stream"
