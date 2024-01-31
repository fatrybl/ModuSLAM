"""
Matches measurement handlers with edges
"""

from dataclasses import dataclass
from typing import Generic, TypeVar

# from slam.frontend_manager.graph.edges.edges import LidarOdometry
# from slam.frontend_manager.handlers.pointcloud_matcher import PointcloudMatcher


@dataclass
class Base:
    id: int

    def __hash__(self):
        return hash(self.id)


@dataclass
class A(Base):
    name: str

    def __hash__(self):
        return hash(self.name)


@dataclass
class C(Base):
    number: float

    def __hash__(self):
        return hash(self.number)


T = TypeVar("T", bound=Base)


class Storage(Generic[T]):
    def __init__(self):
        self.table = set[T]()

    def add(self, item: T) -> None:
        self.table.add(item)

    def __repr__(self):
        return f"{self.table}"


storage = Storage[Base]()

storage.add(A(1, "a"))
storage.add(Base(2))
print(storage)
