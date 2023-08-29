import pytest
from pathlib import Path
from .data_reader_factory_test import DEFAULT_CONFIG_PATH


@pytest.fixture(scope='function', autouse=True)
def clean():
    # Will be executed before the first test
    yield
    # Will be executed after the last test
    Path.unlink(DEFAULT_CONFIG_PATH, missing_ok=True)
