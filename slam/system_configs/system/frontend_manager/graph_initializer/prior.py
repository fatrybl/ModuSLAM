from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class PriorConfig:
    """Prior configuration for the graph initializer."""

    timestamp: int
    vertex_type: str
    edge_factory_name: str
    measurement: tuple[Any, ...]
    measurement_noise_covariance: tuple[float, ...]
    file_path: Path


@dataclass
class GraphInitializerConfig:
    """Prior configuration for the graph initializer."""

    priors: dict[str, PriorConfig]
