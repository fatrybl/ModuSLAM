from dataclasses import dataclass, field

from omegaconf import MISSING


@dataclass
class DataRegimeConfig:
    """Data flow regime."""

    name: str
    start: str = field(kw_only=True, default=MISSING)
    stop: str = field(kw_only=True, default=MISSING)


@dataclass
class TimeLimit:
    """Data flow regime with limited time range."""

    start: int | float
    stop: int | float
    name: str = "TimeLimit"


@dataclass
class Stream:
    """Data flow regime w/o limitations."""

    name: str = "Stream"
