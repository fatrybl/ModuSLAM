from dataclasses import dataclass, field
from typing import Any


@dataclass
class Data:
    timestamps: list = field(default_factory=list)
    measurements: list = field(default_factory=list)
    locations: list = field(default_factory=list)


@dataclass
class Measurement:
    sensor: str
    values: Any


@dataclass
class Element:
    timestamp: int
    measurement: Measurement
    location: dict
