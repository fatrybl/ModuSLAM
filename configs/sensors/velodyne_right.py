from dataclasses import dataclass, field

from .base_sensor_parameters import Parameter


@dataclass
class VelodyneRightParameter(Parameter):
    pose: list[float] = field(default_factory=lambda: [1, 0, 0, 0,
                                                       0, 1, 0, 0,
                                                       0, 0, 1, 0,
                                                       0, 0, 0, 1])
