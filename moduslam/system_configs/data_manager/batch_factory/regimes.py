from dataclasses import dataclass, field

from omegaconf import MISSING


@dataclass
class DataRegimeConfig:
    """Data flow regime."""

    name: str
    start: int = field(kw_only=True, default=MISSING)
    stop: int = field(kw_only=True, default=MISSING)


@dataclass
class TimeLimit:
    """Data flow regime with limited time range."""

    start: int
    stop: int
    name: str = "TimeLimit"


@dataclass
class Stream:
    """Data flow regime w/o limitations."""

    name: str = "Stream"
