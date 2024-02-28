from dataclasses import dataclass


@dataclass
class ElementDistributorConfig:
    """Config for ElementDistributor."""

    sensor_handlers_table: dict[str, list[str]]
