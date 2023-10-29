from dataclasses import dataclass, field
from omegaconf import MISSING


@dataclass
class ParameterConfig:
    pose: list[float] = field(
        metadata={"format": "RBT matrix SE(3)",
                  "description": "Position and rotation of a sensor"},
        default=MISSING)
