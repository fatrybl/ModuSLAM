from dataclasses import dataclass, field


@dataclass
class MemoryAnalyzerConfig:
    """Configures MemoryAnalyzer."""

    batch_memory: float = field(
        metadata={"description": "Memory limit for the batch.", "units": "percent"}
    )
