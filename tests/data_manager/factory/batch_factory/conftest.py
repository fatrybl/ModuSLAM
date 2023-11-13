from pathlib import Path
from typing import Any, Callable, TypeAlias


CURRENT_DIR: Path = Path(__file__).parent
CONFIG_MODULE_DIR: str = "batch_factory.api.conf"
DATASET_CONFIG_NAME: str = "dataset_config"
REGIME_CONFIG_NAME: str = "regime_config"
SENSOR_FACTORY_CONFIG_NAME: str = "sensor_factory_config"
BATCH_FACTORY_CONFIG_NAME: str = "batch_factory_config"

Fixture: TypeAlias = Callable[[Any], Any]
