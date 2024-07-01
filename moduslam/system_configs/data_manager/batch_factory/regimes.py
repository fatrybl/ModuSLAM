from dataclasses import dataclass, field


@dataclass
class TimeLimit:
    """Data flow regime with limited time range."""

    start: int = field(metadata={"help": "Start time in nanoseconds."})
    stop: int = field(metadata={"help": "Stop time in nanoseconds."})
    name: str = "TimeLimit"


@dataclass
class Stream:
    """Data flow regime w/o limitations."""

    name: str = "Stream"
