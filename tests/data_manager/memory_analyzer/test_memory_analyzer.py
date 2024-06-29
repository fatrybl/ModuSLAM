"""Tests for the MemoryAnalyzer."""

from moduslam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer


def test_analyzer():
    analyzer = MemoryAnalyzer(batch_memory_percent=100.0)
    assert analyzer.total_memory > 0
    assert 0 <= analyzer.available_memory_percent <= 100
    assert 0 <= analyzer.used_memory_percent <= 100
    assert 0 <= analyzer.permissible_memory_percent <= 100
