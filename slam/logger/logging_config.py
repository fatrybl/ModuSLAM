"""This module contains the logging configuration for the project."""

from logging.config import dictConfig
from pathlib import Path

LOG_DIR = Path(__file__).parents[2] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
MAIN_LOG = LOG_DIR / "main.log"
DATA_MANGER_LOG = LOG_DIR / "data_manager.log"


CONFIG = {
    "version": 1,
    "loggers": {
        "": {  # root logger
            "level": "NOTSET",
            "propagate": False,
            "handlers": ["console_handler"],
        },
        "main_manager": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console_handler", "file_handler"],
        },
    },
    "handlers": {
        "console_handler": {
            "level": "DEBUG",
            "formatter": "info",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "level": "DEBUG",
            "formatter": "error",
            "class": "logging.FileHandler",
            "filename": MAIN_LOG,
            "mode": "a",
        },
    },
    "formatters": {
        "info": {
            "format": "%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s"
        },
        "error": {
            "format": "%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s"
        },
    },
}

dictConfig(CONFIG)
