from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DatasetConfig:
    """Base dataset configuration."""

    name: str
    url: str
    directory: Path = field(metadata={"description": "path to dataset directory"})
    reader: str = field(metadata={"description": "name of the data reader class"})
