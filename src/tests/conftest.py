"""Paths to test data directories."""

import os
from pathlib import Path

env_var: str | None = os.getenv("SRC_DIR")

if env_var is not None:
    src_dir = Path(env_var)
else:
    src_dir = Path(__file__).resolve().parent.parent

test_data_dir = src_dir / "tests_data"

kaist_custom_dataset_dir = test_data_dir / "kaist_urban_custom_dataset"
kaist_urban30_dataset_dir = test_data_dir / "datasets" / "kaist_urban" / " kaist_urban30"
tum_vie_dataset_dir = test_data_dir / "datasets" / "tum_vie" / "loop_floor_0"
s3e_dataset_dir = test_data_dir / "datasets" / "ros2" / "s3e_playground_2"
