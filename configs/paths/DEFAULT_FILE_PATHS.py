from enum import Enum
from pathlib2 import Path


class ConfigFilePaths(Enum):
    root_path = Path(__file__).parent.parent
    data_manager_config = root_path / "system/data_manager/data_manager.yaml"
