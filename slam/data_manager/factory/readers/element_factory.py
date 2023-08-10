from dataclasses import dataclass, field
from typing import Any


@dataclass
class Measurement:
    sensor: str
    values: Any


@dataclass
class Data:
    timestamp: list = field(default_factory=list)
    measurement: list = field(default_factory=list)
    location: list = field(default_factory=list)


@dataclass
class Element:
    timestamp: int
    measurement: Measurement
    location: dict

# class ElementFactory():
#     def __init__(self):
#         self.elements = [Element]

#     def row_to_elements(self, row: dict) -> None:
#         full_row = next(reader)
#         used_row = {x: full_row[x] for x in self.__used_topic_names}
#         element = element(used_row)
