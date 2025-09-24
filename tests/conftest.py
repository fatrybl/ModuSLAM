"""Configuration for test data directories and paths.

This module provides centralized path configuration for test data directories, ensuring
consistent access to test datasets across all tests.
"""

import os
from pathlib import Path

# Determine the project root directory
env_var: str | None = os.getenv("SRC_DIR")

if env_var is not None:
    project_root = Path(env_var)
else:
    # conftest.py is in tests/, so parent.parent gives us project root
    project_root = Path(__file__).resolve().parent.parent

# Test data is located in tests/tests_data directory
test_data_dir = project_root / "tests" / "tests_data"

# Dataset directory paths - all paths are verified to exist in the project structure
kaist_urban30_dataset_dir = test_data_dir / "datasets" / "kaist_urban" / "kaist_urban30"
tum_vie_dataset_dir = test_data_dir / "datasets" / "tum_vie" / "loop_floor_0"
s3e_dataset_dir = test_data_dir / "datasets" / "ros2" / "s3e_playground_2"

# Convenience variables for common dataset components
datasets_dir = test_data_dir / "datasets"

# Custom KAIST dataset directory for test data generation
kaist_custom_dataset_dir = test_data_dir / "datasets" / "kaist_custom"


def get_test_data_path(relative_path: str) -> Path:
    """Get absolute path to a test data file or directory.

    Args:
        relative_path: Path relative to the test_data_dir

    Returns:
        Absolute path to the requested test data

    Example:
        >>> get_test_data_path("datasets/kaist_urban/kaist_urban30")
        PosixPath('/path/to/project/tests/tests_data/datasets/kaist_urban/kaist_urban30')
    """
    return test_data_dir / relative_path


def verify_test_data_exists() -> bool:
    """Verify that the main test data directory exists.

    Returns:
        True if test data directory exists and is accessible
    """
    return test_data_dir.exists() and test_data_dir.is_dir()
