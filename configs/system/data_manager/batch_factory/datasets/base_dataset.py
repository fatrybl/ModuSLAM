from dataclasses import dataclass, field
from pathlib import Path

from omegaconf import MISSING


@dataclass
class DatasetConfig:
    """
    Base class for any supported dataset.
    """

    name: str = MISSING
    url: str = MISSING
    directory: Path = field(default=MISSING, metadata={"description": "dataset directory"})
    reader: str = field(default=MISSING, metadata={"description": "Name of the data reader class"})
