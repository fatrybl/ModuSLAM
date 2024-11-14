from dataclasses import dataclass, field
from pathlib import Path

from omegaconf import MISSING


@dataclass
class DataRegimeConfig:
    """Data flow regime."""

    name: str
    start: str = field(kw_only=True, default=MISSING)
    stop: str = field(kw_only=True, default=MISSING)


@dataclass
class DataReaders:
    kaist_reader: str = "Kaist Reader"
    tum_vie_reader: str = "Tum Vie Reader"
    ros2_reader: str = "Ros2 Reader"


@dataclass
class DatasetConfig:
    """Base dataset configuration."""

    name: str
    url: str
    directory: Path = field(metadata={"description": "path to dataset directory"})
    reader: str = field(metadata={"description": "name of the data reader class"})


@dataclass
class BatchFactoryConfig:
    """Batch factory configuration."""

    dataset: DatasetConfig
    regime: DataRegimeConfig
    batch_memory_percent: float = field(
        default=90.0, metadata={"help": "RAM-memory percent used for the data batch."}
    )
