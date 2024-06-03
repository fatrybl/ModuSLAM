from dataclasses import dataclass, field


@dataclass
class MemoryAnalyzerConfig:
    """Configuration for the memory analyzer."""

    batch_memory: float = field(
        metadata={"description": "Memory limit for the batch.", "units": "percent"}
    )
