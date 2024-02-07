from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class ElementDistributorConfig:
    """
    Config for ElementDistributor.
    """

    sensor_handlers_table: dict[str, list[str]] = MISSING
