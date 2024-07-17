from dataclasses import dataclass, field

from omegaconf import MISSING


@dataclass
class DataRegimeConfig:
    """Data flow regime."""

    name: str
    start: float = field(kw_only=True, default=MISSING)
    stop: float = field(kw_only=True, default=MISSING)


@dataclass
class TimeLimit:
    """Data flow regime with limited time range."""

    start: int | float
    stop: int | float
    name: str = "TimeLimit"


@dataclass(frozen=True)
class Stream:
    """Data flow regime w/o limitations."""

    name: str = "Stream"
