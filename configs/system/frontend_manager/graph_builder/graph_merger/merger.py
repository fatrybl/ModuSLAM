from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class GraphMergerConfig:
    handler_edge_factory_table: dict[str, str] = MISSING
