from dataclasses import dataclass
from pathlib import Path
from omegaconf import MISSING


@dataclass
class Dataset:
    """
    Base class for any supported dataset.
    """
    name: str = MISSING
    url: str = MISSING
    directory: Path = MISSING
    dataset_type: str = MISSING
