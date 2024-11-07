from dataclasses import dataclass, field

from phd.moduslam.frontend_manager.handlers.base_config import HandlerConfig


@dataclass
class VrsGpsHandlerConfig(HandlerConfig):
    fix_statuses: list[int] = field(
        default_factory=lambda: [4], metadata={"help": "RTK Fix statuses to be used."}
    )
