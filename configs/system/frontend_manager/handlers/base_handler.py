from dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class HandlerConfig:
    """
    Base config for a handler.
    """

    name: str = MISSING
    type_name: str = MISSING
    module_name: str = MISSING
    parameters: dict = MISSING
