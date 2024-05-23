from dataclasses import dataclass, field

from slam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class VrsGpsHandlerConfig(HandlerConfig):
    fix_statuses: list[int] = field(
        default_factory=lambda: [4], metadata={"help": "RTK Fix statuses to be used."}
    )
