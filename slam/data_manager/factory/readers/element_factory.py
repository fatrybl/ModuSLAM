from dataclasses import dataclass, field
from typing import Any


@dataclass
class Measurement:
    sensor: str
    values: Any


@dataclass
class Element:
    timestamp: int
    measurement: Measurement
    location: dict[Any, Any]


@dataclass
class Data:
    elements: list[Element] = field(default_factory=list)
