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

    def __init__(self, config: HandlerConfig) -> None:
        self._name = config.name

    @property
    def name(self) -> str:
        """Name of the handler."""
        return self._name

    @abstractmethod
    def process(self, element) -> Measurement | None: ...
