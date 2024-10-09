from dataclasses import dataclass


@dataclass
class ElementDistributorConfig:
    """Base ElementDistributor configuration."""

    sensor_handlers_table: dict[str, list[str]]
