from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from slam.system_configs.system.frontend_manager.handlers.base_handler import (
    HandlerConfig,
)

if TYPE_CHECKING:
    from slam.frontend_manager.element_distributor.measurement_storage import (
        Measurement,
    )


class Handler(ABC):
    """Base external module."""

    @abstractmethod
    def __init__(self, config: HandlerConfig) -> None: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def process(self, element) -> Measurement | None: ...
