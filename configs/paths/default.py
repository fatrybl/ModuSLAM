from dataclasses import dataclass
from pathlib import Path

@dataclass
class ConfigPaths:
    root_path = Path(__file__).parent.parent
    system_config_dir = root_path / "system"
    sensors_config_dir = root_path / "sensors"
    exoeriments_config_dir = root_path / "experiments"
