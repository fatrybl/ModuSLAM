import os
import tempfile
from pathlib import Path

import pytest

from src.moduslam.map_manager.trajectory import (
    Trajectory,
    load_trajectory_from_txt,
    save_trajectory_to_txt,
)


@pytest.fixture
def sample_trajectory() -> Trajectory:
    return [
        (
            1,
            (
                (1.0, 0.0, 0.0, 0.0),
                (0.0, 1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
            ),
        ),
        (
            2,
            (
                (0.0, -1.0, 0.0, 2.0),
                (1.0, 0.0, 0.0, 3.0),
                (0.0, 0.0, 1.0, 4.0),
                (0.0, 0.0, 0.0, 1.0),
            ),
        ),
    ]


def test_save_and_load_trajectory(sample_trajectory):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file_path = Path(tmp.name)
    try:
        save_trajectory_to_txt(file_path, sample_trajectory)
        loaded_trajectory = load_trajectory_from_txt(file_path)
        assert loaded_trajectory == sample_trajectory
    finally:
        os.remove(file_path)
