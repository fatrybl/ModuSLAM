from dataclasses import dataclass


@dataclass
class HandlerConfig:
    """Base handler configuration."""

    name: str
    type_name: str
    module_name: str
