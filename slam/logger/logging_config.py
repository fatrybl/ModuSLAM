from logging.config import dictConfig
from pathlib import Path

LOG_DIR = Path(__file__).parents[2] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

main_manager_logger = "main_manager"
data_manager_logger = "data_manager"
frontend_manager_logger = "frontend_manager"
backend_manager_logger = "backend_manager"
setup_manager_logger = "setup_manager"
map_manager_logger = "map_manager"
utils_logger = "utils"

run_log_file = LOG_DIR / "run.log"

CONFIG = {
    "version": 1,
    "loggers": {
        main_manager_logger: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console_handler", "rotating_file_handler"],
        },
        data_manager_logger: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console_handler", "rotating_file_handler"],
        },
        frontend_manager_logger: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console_handler", "rotating_file_handler"],
        },
        backend_manager_logger: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console_handler", "rotating_file_handler"],
        },
        setup_manager_logger: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console_handler", "rotating_file_handler"],
        },
        map_manager_logger: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console_handler", "rotating_file_handler"],
        },
        utils_logger: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["console_handler", "rotating_file_handler"],
        },
    },
    "handlers": {
        "console_handler": {
            "formatter": "info",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "rotating_file_handler": {
            "formatter": "error",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": run_log_file,
            "mode": "w",
            "maxBytes": 1000,  # 1KB
            "backupCount": 1,
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
