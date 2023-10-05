from dataclasses import dataclass, field

from omegaconf import MISSING


@dataclass
class MemoryAnalyzer:
    graph_memory: float = field(default=MISSING, metadata={'units': 'percent'})
