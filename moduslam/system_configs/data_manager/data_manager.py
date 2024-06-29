from dataclasses import dataclass

from moduslam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from moduslam.system_configs.data_manager.batch_factory.memory import (
    MemoryAnalyzerConfig,
)


@dataclass
class DataManagerConfig:
    """Data manager configuration."""

    batch_factory: BatchFactoryConfig
    memory_analyzer: MemoryAnalyzerConfig
