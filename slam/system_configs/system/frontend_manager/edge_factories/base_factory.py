from dataclasses import dataclass, field


@dataclass
class NoiseConfig:
    noise_model_name: str
    values: list[float]


@dataclass
class DiagonalNoiseConfig(NoiseConfig):
    """Diagonal noise model config."""

    noise_model_name: str = "Diagonal"
    values: list[float] = field(default_factory=list)


@dataclass
class EdgeFactoryConfig:
    """Base edge factory config."""

    name: str
    type_name: str
    module_name: str
    search_time_margin: int = field(default=0, metadata={"help": "Time margin in nanoseconds."})
