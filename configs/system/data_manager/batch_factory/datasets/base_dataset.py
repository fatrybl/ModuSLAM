from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DatasetConfig:
    """Base class for any supported dataset."""

    name: str
    url: str
    directory: Path = field(metadata={"description": "dataset directory"})
    reader: str = field(metadata={"description": "Name of the data reader class"})
