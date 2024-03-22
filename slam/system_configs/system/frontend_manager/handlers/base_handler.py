from dataclasses import dataclass


@dataclass
class HandlerConfig:
    """Base config for a handler."""

    name: str
    type_name: str
    module_name: str
