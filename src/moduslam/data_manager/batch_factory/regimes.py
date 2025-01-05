from dataclasses import dataclass


@dataclass
class TimeLimit:
    """Data flow regime with limited time range."""

    start: int | float
    stop: int | float
    name: str = "TimeLimit"

    def __post_init__(self):
        if self.start > self.stop:
            raise ValueError("Start timestamp should be not greater than stop timestamp.")


@dataclass
class Stream:
    """Data flow regime w/o limitations."""

    name: str = "Stream"
