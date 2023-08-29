import pytest
from pathlib import Path
from .test_config import PATHS


@pytest.fixture(scope='function', autouse=True)
def clean():
    # Will be executed before the first test
    yield
    # Will be executed after the last test
    for path in PATHS:
        Path.unlink(path, missing_ok=True)
