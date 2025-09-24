from dataclasses import dataclass, field

from moduslam.custom_types.aliases import Vector3
from moduslam.external.handlers_factory.handlers.handler_protocol import HandlerConfig


@dataclass
class VrsGpsHandlerConfig(HandlerConfig):
    fix_statuses: list[int] = field(
        default_factory=lambda: [4], metadata={"help": "RTK Fix statuses to be used."}
    )

    first_position: Vector3 | None = None
