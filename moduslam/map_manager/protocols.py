"""Protocols for the map manager."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class MapFactory(Protocol):
    @property
    def map(self) -> Any:
        """Map instance."""

    def create_map(self, *args, **kwargs) -> None:
        """Creates map instance."""


@runtime_checkable
class MapLoader(Protocol):
    def save(self, *args, **kwargs) -> None:
        """Saves the map."""

    def load(self) -> Any:
        """Loads the map."""


@runtime_checkable
class MapVisualizer(Protocol):
    def visualize(self, *args, **kwargs) -> None:
        """Visualizes the map."""
