"""Tests for the sort_files_numerically function."""

from pathlib import Path

from src.utils.auxiliary_methods import sort_files_numerically


def test_sort_files_numerically():
    file_extension = ".txt"
    files = [Path(f"{i}{file_extension}") for i in [12, 2, 1, 10]]
    expected_sorted_files = [Path(f"{i}{file_extension}") for i in [1, 2, 10, 12]]

    sorted_files = sort_files_numerically(files)

    assert sorted_files == expected_sorted_files
