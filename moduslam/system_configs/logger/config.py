from dataclasses import dataclass
from pathlib import Path


@dataclass
class LoggerConfig:
    """Configuration of the logger."""

    level: str = "INFO"
    logs_directory: Path = Path("logs")
