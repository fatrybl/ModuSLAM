from __future__ import annotations
import logging
import sys

from pathlib import Path
from yaml import safe_load, dump
from slam.utils.exceptions import ConfigFileNotValid

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        self._attributes = dict
        self._file_path = Path

    @property
    def attributes(self) -> dict:
        return self._attributes

    @attributes.setter
    def attributes(self, params: dict) -> None:
        self._attributes = params

    @attributes.deleter
    def attributes(self):
        del self._attributes

    @property
    def file_path(self) -> Path:
        return self._file_path

    @file_path.setter
    def file_path(self, path: Path):
        self._file_path = path
        self._file_name = path.name
        self._file_type = path.suffix

    @file_path.deleter
    def file_path(self) -> None:
        del self._file_path

    def _is_valid(self) -> bool:
        if not self.file_path.exists():
            logger.critical(f"Config file {self.file_path} does not exist")
            return False

        if self._file_type != ".yaml":
            logger.critical(
                f"The type of config file {self._file_type} is not valid")
            return False

        if self.file_path.stat().st_size == 0:
            logger.critical(f"Config file {self.file_path} is empty")
            return False

        return True

    def _read_file(self) -> None:
        try:
            with open(self.file_path, "r") as f:
                self._attributes = safe_load(f)

        except OSError:
            logger.critical(
                f"Config file {self.file_path} is corrupted and has not been loaded properly")
            sys.exit(1)

    @classmethod
    def from_file(cls, file_path: Path) -> Config:
        cfg = Config()
        cfg.file_path = file_path
        if cfg._is_valid():
            cfg._read_file()
            return cfg
        else:
            logger.critical(f'Config file: {file_path}  is not valid')
            raise ConfigFileNotValid

    def to_file(self, file_path: Path) -> None:
        try:
            with open(file_path, 'w') as outfile:
                dump(self._attributes, outfile)
        except OSError:
            logger.exception(f'can not save config to file: {file_path}')
