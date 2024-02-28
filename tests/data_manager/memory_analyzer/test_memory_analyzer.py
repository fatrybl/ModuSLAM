import pytest

from slam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from slam.system_configs.system.data_manager.batch_factory.memory import (
    MemoryAnalyzerConfig,
)


@pytest.fixture
def memory_analyzer():
    config = MemoryAnalyzerConfig(batch_memory=100.0)
    return MemoryAnalyzer(config)


def test_total_memory(memory_analyzer: MemoryAnalyzer):
    assert isinstance(memory_analyzer.total_memory, int)
    assert memory_analyzer.total_memory > 0


def test_available_memory_percent(memory_analyzer: MemoryAnalyzer):
    assert isinstance(memory_analyzer.available_memory_percent, float)
    assert 0 <= memory_analyzer.available_memory_percent <= 100


def test_used_memory_percent(memory_analyzer: MemoryAnalyzer):
    assert isinstance(memory_analyzer.used_memory_percent, float)
    assert 0 <= memory_analyzer.used_memory_percent <= 100


def test_permissible_memory_percent(memory_analyzer: MemoryAnalyzer):
    assert isinstance(memory_analyzer.permissible_memory_percent, float)
    assert 0 <= memory_analyzer.permissible_memory_percent <= 100
