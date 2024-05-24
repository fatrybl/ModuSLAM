from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class PriorConfig:
    """Base prior configuration."""

    timestamp: int
    vertex_type: str
    edge_factory_name: str
    measurement: tuple[Any, ...]
    measurement_noise_covariance: tuple[float, ...]
    file_path: Path


@dataclass
class GraphInitializerConfig:
    """Base graph initializer configuration."""

    priors: dict[str, PriorConfig]
