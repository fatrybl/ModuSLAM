from dataclasses import dataclass


@dataclass
class GraphMergerConfig:
    """Base graph merger configuration."""

    handler_edge_factory_table: dict[str, str]
