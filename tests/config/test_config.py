import pytest
from yaml import safe_dump
from slam.utils.exceptions import ConfigFileNotValid
from pathlib import Path

from slam.utils.config import Config

TEST_DIR = Path(__file__).parent
DEFAULT_CONFIG_PATH = TEST_DIR / "test_config.yaml"
NON_YAML_CONFIG_PATH = TEST_DIR / "test_config.txt"
EMPTY_CONFIG_PATH = TEST_DIR / "test_empty.yaml"
NON_EXISTING_CONFIG_PATH = TEST_DIR / "test_non_existing.yaml"

PATHS = [DEFAULT_CONFIG_PATH,
         NON_YAML_CONFIG_PATH,
         EMPTY_CONFIG_PATH,
         NON_EXISTING_CONFIG_PATH,]

TEST_DICT = {'param1': 'some_test_param',
             'param2': 1234}

"""
Fail cases for _is_valid() method:
1) File does not exist
2) File is empty
3) File extension is not ".yaml"
Success cases for _is_valid() method:
1) File is correct
"""


def create_config_file(cfg: dict, path: Path) -> None:
    """
    if cfg is None: creates empty config file
    """
    if cfg:
        with open(path, 'w') as outfile:
            safe_dump(cfg, outfile)
    else:
        open(path, 'a').close()


scenario1 = (TEST_DICT, DEFAULT_CONFIG_PATH, True)
scenario2 = (TEST_DICT, NON_YAML_CONFIG_PATH, False)
scenario3 = (None, EMPTY_CONFIG_PATH, False)

scenarios = [scenario1, scenario2, scenario3]


@pytest.mark.parametrize(
    ("cfg", "path", "expected_output"), scenarios
)
def test_is_valid(cfg: dict, path: Path, expected_output: bool):
    create_config_file(cfg, path)
    cfg = Config()
    cfg.file_path = path
    assert cfg._is_valid() == expected_output


def test_is_valid_for_none_existing_path():
    cfg = Config()
    cfg.file_path = NON_EXISTING_CONFIG_PATH
    Path.unlink(NON_EXISTING_CONFIG_PATH, missing_ok=True)
    assert cfg._is_valid() == False


def test_from_file_success():
    create_config_file(TEST_DICT, DEFAULT_CONFIG_PATH)
    cfg = Config.from_file(DEFAULT_CONFIG_PATH)
    assert isinstance(cfg, Config)


def test_from_file_fail():
    create_config_file(TEST_DICT, NON_YAML_CONFIG_PATH)
    with pytest.raises(ConfigFileNotValid):
        cfg = Config.from_file(NON_YAML_CONFIG_PATH)
