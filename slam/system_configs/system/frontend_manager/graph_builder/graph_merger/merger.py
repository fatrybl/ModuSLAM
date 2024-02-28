from dataclasses import dataclass


@dataclass
class GraphMergerConfig:
    handler_edge_factory_table: dict[str, str]
