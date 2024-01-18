from dataclasses import dataclass, field

from .base_sensor_parameters import ParameterConfig


@dataclass
class EncoderParameter(ParameterConfig):
    pose: list[float] = field(default_factory=lambda: [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
