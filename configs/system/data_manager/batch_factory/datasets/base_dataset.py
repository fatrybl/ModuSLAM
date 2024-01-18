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
    type: str = field(default=MISSING, metadata={"description": "type of a supported dataset"})
