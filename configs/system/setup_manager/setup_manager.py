from dataclasses import dataclass, field

from .sensor_factory import SensorFactory


@dataclass
class SetupManager:
    """
    Config for SetupManager.
    """
    sensor_factory: SensorFactory = field(default_factory=SensorFactory)
