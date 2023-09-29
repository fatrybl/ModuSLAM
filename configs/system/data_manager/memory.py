from dataclasses import dataclass, field


@dataclass
class MemoryAnalyzer:
    graph_memory: float = field(default=30, metadata={'units': 'percent'})
