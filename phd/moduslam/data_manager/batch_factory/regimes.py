from dataclasses import dataclass


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
