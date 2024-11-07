from dataclasses import dataclass


@dataclass
class HandlerConfig:
    """Base handler configuration."""

    sensor_name: str
