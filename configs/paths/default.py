from dataclasses import dataclass
from pathlib import Path


@dataclass
class PathsConfig:
    root_path: Path = Path(__file__).parent.parent
    system_config_dir: Path = root_path / "system"
    sensors_config_dir: Path = root_path / "sensors"
    exoeriments_config_dir: Path = root_path / "experiments"
