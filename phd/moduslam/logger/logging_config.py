"""Configures the logger for the moduslam package."""

from logging.config import dictConfig
from pathlib import Path

from moduslam.system_configs.logger.config import LoggerConfig

# global logger names
main_manager = "main_manager"
data_manager = "data_manager"
frontend_manager = "frontend_manager"
backend_manager = "backend_manager"
setup_manager = "setup_manager"
map_manager = "map_manager"
utils = "utils"


def get_config(log_file: Path, level: str = "INFO") -> dict:
    """Returns a dictionary with the logging configuration.

    Args:
        log_file: file to write the logs to.

        level: logging level. Default is INFO.

    Returns:
        logging configuration.
    """

    config = {
        "version": 1,
        "loggers": {
            main_manager: {
                "level": level,
                "handlers": ["console", "rotating_file"],
            },
            data_manager: {
                "level": level,
                "handlers": ["console", "rotating_file"],
            },
            frontend_manager: {
                "level": level,
                "handlers": ["console", "rotating_file"],
            },
            backend_manager: {
                "level": level,
                "handlers": ["console", "rotating_file"],
            },
            setup_manager: {
                "level": level,
                "handlers": ["console", "rotating_file"],
            },
            map_manager: {
                "level": level,
                "handlers": ["console", "rotating_file"],
            },
            utils: {
                "level": level,
                "handlers": ["console", "rotating_file"],
            },
        },
        "handlers": {
            "console": {
                "formatter": "colored",
                "class": "colorlog.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "rotating_file": {
                "formatter": "error",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_file,
                "mode": "w",
                "maxBytes": 1000,  # 1KB
                "backupCount": 1,
            },
        },
        "formatters": {
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(asctime)s%(reset)s - %(log_color)s%(levelname)s%(reset)s - %(module)s:: %(message)s",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "light_red",
                    "CRITICAL": "red",
                },
            },
            "info": {"format": "%(asctime)s-%(levelname)s-%(name)s::%(module)s:: %(message)s"},
            "error": {
                "format": "%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(funcName)s|%(lineno)s:: %(message)s"
            },
        },
    }

    return config


def setup_logger(config: LoggerConfig) -> None:
    """Sets up the logger with the specified configuration.

    Args:
        config: logger configuration.
    """
    logs_directory = config.logs_directory
    logs_directory.mkdir(exist_ok=True)
    log_file = logs_directory / "run.log"
    cfg = get_config(log_file, config.level)
    dictConfig(cfg)
