"""Base configurations for map manager."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MapFactoryConfig:
    """Base configuration for map factory."""

    map_type: str


@dataclass
class MapLoaderConfig:
    """Base configuration for map loader."""

    map_type: str
    directory: Path = field(default_factory=Path, metadata={"help": "Directory to save the map."})


@dataclass
class MapManagerConfig:
    """Base configuration for map manager."""

    map_factory: MapFactoryConfig
    map_loader: MapLoaderConfig
