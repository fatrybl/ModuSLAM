
from abc import ABC
from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class Regime(ABC):
    """
    Abstract regime of data flow.
    """
    name: str = MISSING


@dataclass
class TimeLimit(Regime):
    """
    Data flow is limited by time range.
    """
    start: int = MISSING
    stop: int = MISSING
    name: str = "TimeLimit"


@dataclass
class Stream(Regime):
    """
    Free data flow: each measurement is processed sequantially.
    """
    name: str = "Stream"
